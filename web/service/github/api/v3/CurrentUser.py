#!python3
#encoding:utf-8
class CurrentUser(object):
    def __init__(self, db, username):
        self.__db = db
        self.__username = None
        self.Change(username)
        self.__password = None
        self.__ssh_host = None
        self.__mail = None

    def __GetRepoDb(self):
        return self.__db.repos[self.Name]
    RepoDb = property(__GetRepoDb)

    def __GetSelectableUsernames(self):
        names = []
        for a in self.__db.account['Accounts'].find():
            names.append(a['Username'])
        return names
    SelectableUsernames = property(__GetSelectableUsernames)
    
    def __GetName(self):
        return self.__username
    def Change(self, username):
        if None is not self.__db.account['Accounts'].find_one(Username=username):
            self.__username = username        
    Name = property(__GetName, Change)
    
    def __GetPassword(self):
        return self.__db.account['Accounts'].find_one(Username=self.Name)['Password']
    Password = property(__GetPassword)
    
    def __GetMailAddress(self):
        return self.__db.account['Accounts'].find_one(Username=self.Name)['MailAddress']
    MailAddress = property(__GetMailAddress)
    
    def __GetSshHost(self):
        return "github.com.{0}".format(self.Name)
    SshHost = property(__GetSshHost)
    
    def __GetOtp(self):
        # 2FA-Secretから算出する
        return self.__otp
    Otp = property(__GetOtp)
    
    def GetAccessToken(self, scopes=None):
        sql = "SELECT * FROM AccessTokens WHERE AccountId == {0}".format(self.__db.account['Accounts'].find_one(Username=self.Name)['Id'])
        if not(None is scopes):
            sql = sql + " AND ("
            for s in scopes:
                sql = sql + "(',' || Scopes || ',') LIKE '%,{0},%'".format(s) + " OR "
            sql = sql.rstrip(" OR ")
            sql = sql + ')'
        return self.__db.account.query(sql).next()['AccessToken']

    # 将来的には拡張したい
    # * OTP対応
    # * プロフィールなどユーザ情報の設定
    # * GitHubサーバとの連動(Sync()メソッドでAPIから取得しDBを更新する)
