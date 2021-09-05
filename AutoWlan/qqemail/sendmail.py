from .my_email import my_email
import time

def blog_updating_remind():
    theme = "Qingren's blog updating!"
    content = "Welcome to visit https://qingrenn.github.io/"
    emailObj = my_email()
    emailObj.sendmail(theme, content)
    print("blog updating reminding is successful ...")

def wlan_login_remind(ip):
    theme = f"登陆提醒"
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    content = f"姚清仁的ubuntu已经登陆, IP:{ip}"
    emailObj = my_email()
    emailObj.sendmail(theme, content)

if __name__ == "__main__":
    # blog_updating_remind()
    wlan_login_remind("ttt.ttt.tt.tt")