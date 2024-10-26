遵循 WTFPL V2 licence

## 本项目是一个简陋的用于将pdf反色的工具，提供的是服务端代码，可用于服务端

- 已知问题： linux 操作系统上的 Ghostscript 存在部分字体编码问题，比如由 LaTeX 编译的 pdf 处理后文字层复制会出现乱码，不知道怎么解决。在 windows 上运行未复现。

### 使用说明：
- clone 项目
- 安装所需依赖
- 在 https://www.ghostscript.com/releases/gsdnld.html 下载 Ghostscript 依赖项，下载对应版本，并添加到环境变量中。比如 windows 中添加 `C:\Program Files\gs\gs10.04.0\bin\` 到系统 path 中。
- 如果未添加到环境变量中，需要手动修改 app.py 的第 30 行，修改 `"gswin64c.exe"` 为你的二进制文件所在路径。
- 如希望本地使用批量处理，可自行查看 app.py 中的部分实现逻辑，可以将其抽离为非服务端程序。
- 如果希望运行在服务端生产环境，请注意定时清理 uploads 和 outputs 文件夹。同时不建议直接运行 debug 的 flask 程序，应使用 Gunicorn 或 uWSGI 。
