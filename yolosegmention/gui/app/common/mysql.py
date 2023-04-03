"""
@Project ：Graduation-Project-Fluent 
@File    ：mysql.py
@Author  ：X0RB64
@Date    ：2023/04/02 13:41 
"""
import datetime
import time
from hashlib import sha256

import pymysql

from yolosegmention.exceptions import SqlException, SqlCannotConnectException, SqlNoMatchException, RuntimeException


class Mysql:
    Host: str = 'localhost'
    Port: int = 3306
    User: str = 'graduation_db_user'
    Password: str = '123456'
    Database: str = 'graduationdb'
    Charset: str = 'utf8'
    Dirty_Stuff = ["\"", "\\", "/", "*", "'", "=", "#", ";", "<", ">", "+", "%", "$", "(", ")", "%", "@", "!", "?"]

    def __init__(self):
        try:
            self._connect = pymysql.Connect(
                host=self.Host,
                port=self.Port,
                user=self.User,
                password=self.Password,
                database=self.Database,
                charset=self.Charset,
            )
            self._cursor = self._connect.cursor()
        except pymysql.err.OperationalError:
            raise SqlCannotConnectException()

    def _detectDirtyChar(self, value):
        value = str(value)
        for stuff in self.Dirty_Stuff:
            if stuff in value:
                raise SqlException('存在非法字符！')

    def query(self, formatSql: str, *args) -> tuple:
        return self._cursor.execute(formatSql, args), self._cursor.fetchall()

    def _queryByUsername(self, username: str, *fields) -> str:
        fields = ','.join(fields)
        self._detectDirtyChar(username)
        self._detectDirtyChar(fields)
        res = self.query(f'SELECT {fields} FROM USER WHERE USERNAME=%s;', username)
        if res[0] == 1:
            return res[1][0]
        elif res[0] == 0:
            raise SqlNoMatchException()
        elif res[0] > 1:
            raise SqlException('数据库信息异常！')
        else:
            raise RuntimeException("Unreachable code!")

    def _getSalt(self, username: str) -> str:
        return self._queryByUsername(username, 'SALT')[0]

    def auth(self, username: str, password: str) -> tuple[int, str, str, str]:
        try:
            salt = self._getSalt(username)
            password = sha256((password + salt).encode()).hexdigest()
            res = self._queryByUsername(username, 'PASSWORD', 'PERMISSION', 'NICKNAME', 'UUID')
        except SqlNoMatchException:
            return False, '', '', ''
        else:
            return password == res[0], res[1], res[2], res[3]

    def queryCaseRecord(self, patientUUID: str) -> dict:
        patientInfo = self.query('SELECT `NAME`, `GENDER`, `AGE` FROM `PATIENT` WHERE `UUID`=%s;', patientUUID)
        res = self.query('SELECT `RECORD`, `TIME`, `NICKNAME` FROM `CASE`,`USER` WHERE `PATIENT`=%s AND USER.UUID=CASE.DOCTOR ORDER BY `TIME` ASC;', patientUUID)
        if patientInfo[0] == 0:
            raise SqlNoMatchException()
        elif patientInfo[0] > 1:
            raise SqlException('错误！数据库异常，请立即报告管理员处理！')
        elif patientInfo[0] == 1:
            return {
                'name': patientInfo[1][0][0],
                'gender': patientInfo[1][0][1],
                'age': patientInfo[1][0][2],
                'num': res[0],
                'records': res[1]
            }
        else:
            raise RuntimeException('Unreachable code!')

    def _insert(self, table: str, **kwargs) -> bool:
        """
        :param table: 表名
        :param kwargs: 字典，{字段名: 值}
        :return:
        """
        itemNum = len(kwargs)
        if itemNum == 0:
            raise RuntimeException('错误的参数数量！必须传入至少一个field-value键值对')
        # 检测脏字符
        self._detectDirtyChar(table)
        for key in kwargs:
            self._detectDirtyChar(key)
            self._detectDirtyChar(kwargs[key])

        field = f"`{table}`({', '.join(['`' + field + '`' for field in kwargs.keys()])})"
        value = f"VALUE({('%s ' * itemNum).rstrip().replace(' ', ', ')})"
        try:
            res = self._cursor.execute(f"INSERT INTO {field} {value};", [*kwargs.values()])
            self._connect.commit()
        except pymysql.err.OperationalError:
            raise SqlException(f'参数中含有{table}中不存在的字段！')
        else:
            if res == 1:
                return True
            else:
                raise SqlException('错误！数据库异常，请立即报告管理员处理！')

    def addNewCase(self, record: str, doctorNickname: str, patientUUID: str) -> bool:
        _time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return self._insert(
            'CASE',
            record=record,
            time=_time,
            doctor=doctorNickname,
            patient=patientUUID
        )

    def addNewPatient(self, patientUUID: str, name: str, gender: str, age: int) -> bool:
        if gender not in ['male', 'female']:
            raise RuntimeException(f'{gender}不是一个gender的合法值！gender应该为"male"或"female"！')
        return self._insert(
            'PATIENT',
            uuid=patientUUID,
            name=name,
            gender=gender,
            age=age
        )

    def __del__(self):
        self._cursor.close()
        self._connect.close()
