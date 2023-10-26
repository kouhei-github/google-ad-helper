from passlib.context import CryptContext

class Hash:
    """

    クラス Hash

    このクラスは、bcrypt アルゴリズムを使用してパスワードをハッシュ化し、検証するメソッドを提供します。

    属性
        pwd_ctx (CryptContext)： bcrypt アルゴリズムを持つ CryptContext クラスのインスタンス。

    メソッド：
        bcrypt(password: str) -> str：
            bcrypt アルゴリズムを使ってプレーンパスワードをハッシュする。

            引数
                password (str)： ハッシュ化されるプレーンパスワード。

            戻り値
                str： ハッシュ化されたパスワード。

        verify(hashing_password: str, plain_password: str) -> bool：
            指定されたプレーンパスワードがハッシュ化されたパスワードと一致するか検証する。

            引数
                hashing_password (str)： 比較するハッシュ化されたパスワード。
                plain_password (str)： 検証されるプレーンパスワード。

            戻り値
                ブール値： プレーンパスワードがハッシュ化されたパスワードと一致すれば真、そうでなければ偽。

    """
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    @classmethod
    def bcript(cls, password: str) -> str:
        """
        引数
            password (str)： ハッシュ化される平文のパスワード。

        戻り値
            str： ハッシュ化されたパスワード。

        """
        return cls.pwd_ctx.hash(password)

    @classmethod
    def verify(cls, hashing_password: str, plain_password: str) -> bool:
        """
        指定されたプレーンパスワードがハッシュ化されたパスワードと一致するかどうかを検証する。

        引数
            hashing_password (str)： 比較するハッシュ化されたパスワード。
            plain_password (str)： 検証されるプレーンパスワード。

        戻り値
            ブール値： プレーンパスワードがハッシュ化されたパスワードと一致すれば真。そうでなければ偽。
        """
        return cls.pwd_ctx.verify(plain_password, hashing_password)
