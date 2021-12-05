from chatbot.utils.emojis import cats, cool


def hello():
    return "Hi, glad to see you looking so good today!"


def hi():
    return "Hi you!!! {}".format(cool())


cmds = {"cats": cats, "hello": hello, "hi": hi}
