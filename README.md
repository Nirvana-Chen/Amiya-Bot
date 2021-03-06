# Amiya-Bot

> 基于 [mirai-console](https://github.com/mamoe/mirai-console) 和 [mirai-api-http](https://github.com/project-mirai/mirai-api-http) 的QQ聊天机器人<br>
> 本质为一个 websocket 客户端

> 名字源于游戏 [《明日方舟》](https://ak.hypergryph.com/) 的女主角"阿米娅"，其主题与核心功能也和游戏相关。

    「博士，能再见到您……真是太好了。今后我们同行的路还很长，所以，请您多多关照！」 -- 阿米娅

## 声明

- Amiya-Bot 是在《明日方舟》爱好者群体中诞生的以便捷功能为主的聊天机器人
- 本项目拒绝加入与金钱相关的功能，并在遵守法律法规且符合社会主义核心价值观的前提下使用
- 创建者需承诺不得使用本项目进行**任何形式的盈利行为**
- 本项目不承担因违反上述所带来的一切后果

## 已完成的功能

Amiya 的基础功能可以通过在QQ里向 Amiya 发送 `Amiya有什么功能` 来获得功能指引<br>
管理员功能请阅读代码 `message/replies/admin.py` 理解使用方法<del>(懒)</del>

- 信赖值与心情系统
- 查询干员精英化材料
- 查询干员专精材料
- 查询干员语音资料
- 查询敌方单位资料
- 查询材料怎么获得
- 理智恢复提醒
- 合成玉计算
- 公招查询
    - 普通标签查询
    - 图像识别
- 模拟抽卡
    - 详情模式
    - 略缩模式
- 查看明日方舟微博动态
    - 查询微博
    - 自动推送新微博
- 管理员命令
    - 群发公告

## 准备

- 想要创建自己的 Amiya，建议拥有一定编程基础，否则以下说明将难以理解
- 建议先了解 [mirai-console](https://github.com/mamoe/mirai-console)
  以及其插件 [mirai-api-http](https://github.com/project-mirai/mirai-api-http)
  以便理解源码
    - 关于 [mirai-api-http](https://github.com/project-mirai/mirai-api-http) 的使用请到官方 Github 下查看
- 需要 python 3.7+
- 需要 Mysql 8.0+

## 注意

本项目代码含有以下特点

- 注释较少（会慢慢补充）
- 通过遍历文件的类加载方法
- 通过线程而非协程的异步实现方式
- 强制重启进程

## 开始使用

1. 必须先前往仓库 [Amiya-Bot-resource](https://github.com/vivien8261/Amiya-Bot-resource) 并根据说明完成资源导入
2. 安装 python 依赖

```bash
pip install -r requirements.txt
```

3. 配置 `config.json`

```json5
{
    // 机器人 QQ 号和密码
    "self_id": 1515361402,
    "self_passwords": "",
    // 管理员 QQ 号
    "admin_id": 826197021,
    // 是否使用 MiraiOK
    "mirai_ok": true,
    // 如果是自己配置的mirai-api-http，需要将对应的authKey复制过来
    // 路径为config/MiraiApiHttp/setting.yml
    // 使用 MiraiOK 请忽略
    "authKey": "AMIYARESTART",
    "server": {
        // mirai-api-http 服务配置
        "server_ip": "127.0.0.1",
        "server_port": 8060
    },
    "database": {
        // 数据库配置
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "amiya520",
        "db": "amiya"
    },
    "baidu_cloud": {
        // 百度智能云配置
        "enable": true,
        "app_id": "2152****",
        "api_key": "MM5pPVBBj***************",
        "secret_key": "XRfGzEZufj1MdNKyz***************"
    },
    "message": {
        // 消息指令的频率限制
        "limit": {
            "seconds": 10,
            "max_count": 3
        },
        // 文字回复的最大字符长度，超出则会转为图片发送
        "reply_text_max_length": 100
    },
    "close_beta": {
        // 是否启用封闭测试
        "enable": false,
        "group_id": 852191455
    }
}
```

4. 启动 Amiya 入口程序
    - （非常重要）若不使用 [资源文件](https://github.com/vivien8261/Amiya-Bot-resource)
      说明里的 MiraiOK，请在该步骤前，启动好自己的 mirai-console 和加载插件 mirai-api-http，并修改配置`"mirai_ok": false`

```bash
python amiya.py
```

5. 短暂的启动过程后，若控制台显示了 websocket 连接成功，表示 Amiya 启动成功
    - 若使用了 MiraiOK ，还会额外启动一个窗口

```
...
websocket connecting success
```

6. 现在，唤醒你的 Amiya 吧！

## 功能测试方式

- 快速启动
    - 不需要启动`mirai-console`
    - 直接运行脚本`quickStart.py`并带上参数`Test`
    - 然后在控制台模拟交互

```bash
python quickStart.py Test
```

- 实际环境的封闭测试
    - 配置`config.json`里的封闭测试相关项
    - 再通过上述步骤启动 Amiya
    - 之后，Amiya 仅会回应封闭测试指定的群

```json5
{
    "close_beta": {
        // 启用封闭测试
        "enable": true,
        // 指定测试群号
        "group_id": 852191455
    }
}
```

## 功能使用注意

- **禁言会导致 Amiya 退群！！！**
- 要保证一些功能的使用，请导入 [资源文件](https://github.com/vivien8261/Amiya-Bot-resource) 中的`data.sql`
    - 建议手动更新一次以保证使用最新的数据
- 手动更新数据，最简单的方法，在根目录创建任意 python 脚本并运行以下代码
    - 或者直接在快速启动中输入`update`执行更新
    - 更新会扫描所有未保存的数据，首次更新数据视网速情况可能需要一定的耗时

```python
from modules.gameData import GameData

if __name__ == '__main__':
    GameData().update()
```

- 要使用抽卡功能，请在更新数据后，在数据表`t_pool`内维护卡池信息（`data.sql`带有一部分卡池数据）
- 自然语言处理方法和公招图像识别需要调用 [百度智能云](https://cloud.baidu.com/)
  的接口，如需使用需要自行申请并配置`config.json`

```json5
{
    "baidu_cloud": {
        // 是否启用百度智能云接口
        "enable": false,
        // APP ID
        "app_id": "",
        // API KEY
        "api_key": "",
        // SECRET KEY
        "secret_key": ""
    }
}
```

- 为了防止打招呼时同时唤起了其他机器人回复，而其他机器人又触发了 Amiya 的回复导致循环发生，造成不可控的局面，请务必设置消息限制，在被其他机器人触发循环时及时制止

```json5
{
    "message": {
        // 此处示例为 10 秒内不能超过 3 次指令
        "limit": {
            "seconds": 10,
            "max_count": 3
        }
    }
}
```

## 如何维护

- Amiya 带有**自动更新**功能，会在每天凌晨4点和16点执行以下操作：
    - 重置签到和心情值（仅4点）
    - 清除缓存数据
    - 更新干员数据
    - 重启主程序
- 干员语音资料和敌人数据为即时从 wiki 获取，不需要维护
- 卡池目前需要手动到数据表`t_pool`维护，维护好的卡池可以通过 Amiya 切换卡池的功能进行更换
    - `Tips:` Pickup 的干员可以是虚构的不存在的干员，因为抽卡命中 Pickup 时，是直接使用 Pickup 字段的干员而非从干员表获取

```mysql
-- 新卡池数据插入语句示例
INSERT INTO t_pool (pool_name, pickup_6, pickup_5, pickup_4, limit_pool)
VALUES ('银灰色的荣耀',
        '银灰',
        '初雪,崖心',
        '角峰',
        0)
```

- 在有干员增加的版本，Amiya 在自更新前，需手动配置更新文件`resource/config/update_config.json`，以便在自更新时能正确获取数据

```json5
// 比如当《集成战略》有新干员增加时，在无法抽卡获取的干员对应的列表里添加新干员名
// 否则更新新数据后，干员会被归类到可获取的干员，造成抽卡异常产出
{
    "roguelike_only": [
        "预备干员-近战",
        "预备干员-狙击",
        "预备干员-后勤",
        "预备干员-术师",
        "Sharp",
        "Stormeye",
        "Pith",
        "Touch"
    ]
}
```

- 任何配置改动后需重启 Amiya 后生效，手动重启 Amiya 只需要重新运行`amiya.py`即可
    - 或者使用管理员命令`Amiya重启`
- 要关闭 Amiya，直接关闭 Amiya 的窗口和 mirai-console 即可

## 贡献

- 本项目欢迎 dalao 加入，拯救萌新，刻不容缓！
- 如果有更多的建议或 BUG 反馈，请提交到`issue`或官方QQ群`362165038`
- 你的`star`将会成为 Amiya 成长的经验值

## TODO

- [ ] 修复语音
- [ ] 完善群事件
- [ ] WEB后台管理系统
- [ ] <del>与明日方舟主题不相关的功能</del>

## 鸣谢

部分功能的信息需要从各大渠道获取，特鸣谢以下网站

- [KokodaYo](https://www.kokodayo.fun/)
- [明日方舟官方微博](https://m.weibo.cn/u/6279793937)
- [PRTS - 玩家自由构筑的明日方舟中文Wiki](http://prts.wiki/)
