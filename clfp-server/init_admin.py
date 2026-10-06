# -*- coding: utf-8 -*-
"""把指定账号设为管理员（演示前运行一次）。

用法：
    python init_admin.py
然后按提示输入学号/工号。
"""
from database import SessionLocal
import models


def main():
    account = input("请输入要设为管理员的学号/工号：").strip()
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.account == account).first()
        if user is None:
            print("未找到该账号，请先注册。")
            return
        user.role = "admin"
        db.commit()
        print(f"已将 {user.name}（{account}）设为管理员。")
    finally:
        db.close()


if __name__ == "__main__":
    main()
