from json import dump, load
from pathlib import Path
from platform import system
from shutil import move
from .static import ROOT, USERAGENT

__all__ = ["Settings"]


class Settings:
    # 默认配置参数
    default = {
        "mapping_data": {},  # 账号备注映射数据
        "work_path": "",  # 工作目录路径
        "folder_name": "Download",  # 下载文件夹名称
        "name_format": "发布时间 作者昵称 作品标题",  # 文件命名格式
        "user_agent": USERAGENT,  # 请求头
        # "a_user_agent": USERAGENT,  # 请求头
        # "b_user_agent": USERAGENT,  # 请求头
        "cookie": "",  # Cookie
        "proxy": None,  # 代理设置
        "timeout": 10,  # 超时时间(秒)
        "chunk": 1024 * 1024 * 2,  # 下载块大小(字节)
        "max_retry": 5,  # 最大重试次数
        "record_data": False,  # 是否记录作品数据
        "image_format": "JPEG",  # 图文作品格式
        "image_download": True,  # 是否下载图文
        "video_download": True,  # 是否下载视频
        "live_download": True,  # 是否下载动图
        "folder_mode": True,  # 文件夹归档模式
        "download_record": True,  # 是否记录下载历史
        "author_archive": True,  # 是否按作者归档
        "write_mtime": False,  # 是否写入修改时间
        "download_desc": True,  # 是否下载文案内容
        "language": "zh_CN",  # 语言设置
        "script_server": False,  # 是否启用脚本服务器
    }
    # 根据操作系统设置编码格式
    encode = "UTF-8-SIG" if system() == "Windows" else "UTF-8"
    # 配置说明文档内容
    readme_content = """# XHS-Downloader 配置项说明 (`settings.json`)

本文档详细解释了 `settings.json` 文件中每个配置项的作用，以帮助您更好地自定义程序行为。

---

### 文件与路径 (`File & Path`)

-   **`work_path`**
    -   **说明**: 程序的工作目录，所有下载的文件、数据记录和临时文件都将保存在这个目录下。
    -   **类型**: `字符串` (路径)
    -   **默认值**: `""` (空字符串), 表示使用程序所在的根目录。
    -   **示例**: `"D:\\Downloads\\XHS"`

-   **`folder_name`**
    -   **说明**: 在 `work_path` 下，用于存放最终下载作品的文件夹名称。
    -   **类型**: `字符串`
    -   **默认值**: `"Download"`

-   **`name_format`**
    -   **说明**: 下载的作品文件的命名格式。您可以组合不同的占位符来定义自己喜欢的格式。
    -   **可用占位符**: `发布时间`, `作者昵称`, `作品标题`, `作品ID` 等。
    -   **类型**: `字符串`
    -   **默认值**: `"发布时间 作者昵称 作品标题"`

---

### 下载控制 (`Download Control`)

-   **`image_download`**
    -   **说明**: 是否下载图文类型的作品。如果设置为 `false`，程序将跳过所有图文作品的下载。
    -   **类型**: `布尔值` (`true` / `false`)
    -   **默认值**: `true`

-   **`video_download`**
    -   **说明**: 是否下载视频类型的作品。如果设置为 `false`，程序将跳过所有视频作品的下载。
    -   **类型**: `布尔值` (`true` / `false`)
    -   **默认值**: `true`

-   **`live_download`**
    -   **说明**: 是否下载图文作品中的“动图”（通常是 `.gif` 或视频格式）。
    -   **类型**: `布尔值` (`true` / `false`)
    -   **默认值**: `true`

-   **`download_desc`**
    -   **说明**: 是否在下载作品的同时，创建一个 `.txt` 文件来保存作品的文案信息（标题、内容、标签等）。
    -   **类型**: `布尔值` (`true` / `false`)
    -   **默认值**: `true`

-   **`image_format`**
    -   **说明**: 下载图片时希望保存的格式。`AUTO` 会根据原始格式自动选择。
    -   **可选值**: `"AUTO"`, `"PNG"`, `"WEBP"`, `"JPEG"`, `"HEIC"`
    -   **类型**: `字符串`
    -   **默认值**: `"JPEG"`

---

### 归档与记录 (`Archive & Record`)

-   **`folder_mode`**
    -   **说明**: 文件夹归档模式。如果设置为 `true`，每个作品的所有文件（图片、视频、文案）都会被保存在一个以作品标题命名的独立文件夹中。如果为 `false`，所有文件将直接保存在 `folder_name` 文件夹下。
    -   **类型**: `布尔值` (`true` / `false`)
    -   **默认值**: `true`

-   **`author_archive`**
    -   **说明**: 是否在 `folder_name` 文件夹内，再根据作者的昵称创建一层子文件夹来存放其所有作品。
    -   **类型**: `布尔值` (`true` / `false`)
    -   **默认值**: `true`

-   **`download_record`**
    -   **说明**: 是否记录已下载作品的 ID。开启后，程序会跳过已经下载过的作品，避免重复下载。
    -   **类型**: `布尔值` (`true` / `false`)
    -   **默认值**: `true`

-   **`record_data`**
    -   **说明**: 是否记录作品的详细元数据（如点赞数、评论数等）。这些数据会保存在一个数据库文件中，供未来可能的分析使用。
    -   **类型**: `布尔值` (`true` / `false`)
    -   **默认值**: `false`

-   **`write_mtime`**
    -   **说明**: 是否将下载的文件的“修改时间”设置为作品的原始发布时间。
    -   **类型**: `布尔值` (`true` / `false`)
    -   **默认值**: `false`

---

### 网络设置 (`Network`)

-   **`user_agent`**
    -   **说明**: 向小红书服务器发送请求时使用的 User-Agent。
    -   **类型**: `字符串`
    -   **默认值**: 一个内置的 Chrome User-Agent。

-   **`cookie`**
    -   **说明**: 用于请求小红书网页版的 Cookie。虽然程序无需登录即可工作，但提供一个有效的 Cookie 有时可以获取更稳定的访问。
    -   **类型**: `字符串`
    -   **默认值**: `""`

-   **`proxy`**
    -   **说明**: 用于网络请求的代理服务器。
    -   **类型**: `字符串` 或 `null`
    -   **默认值**: `null` (不使用代理)
    -   **示例**: `"http://127.0.0.1:7890"`

-   **`timeout`**
    -   **说明**: 网络请求的超时时间（单位：秒）。
    -   **类型**: `整数`
    -   **默认值**: `10`

-   **`chunk`**
    -   **说明**: 下载文件时，每次从服务器获取的数据块大小（单位：字节）。
    -   **类型**: `整数`
    -   **默认值**: `2097152` (即 2MB)

-   **`max_retry`**
    -   **说明**: 当网络请求失败时，程序将尝试重新请求的最大次数。
    -   **类型**: `整数`
    -   **默认值**: `5`

---

### 其他 (`Miscellaneous`)

-   **`language`**
    -   **说明**: 程序的界面语言。
    -   **可选值**: `"zh_CN"` (简体中文), `"en_US"` (English)
    -   **类型**: `字符串`
    -   **默认值**: `"zh_CN"`

-   **`script_server`**
    -   **说明**: 是否启用脚本服务器。这是一个高级功能，允许通过 API 与程序交互。
    -   **类型**: `布尔值` (`true` / `false`)
    -   **默认值**: `false`

-   **`mapping_data`**
    -   **说明**: 内部使用的账号备注映射数据，不建议手动修改。
    -   **类型**: `对象`
    -   **默认值**: `{}`
"""

    def __init__(self, root: Path = ROOT):
        """初始化Settings类

        Args:
            root: 设置文件的根目录路径,默认为ROOT
        """
        # 设置文件路径
        self.name = "settings.json"
        self.root = root
        self.path = root.joinpath(self.name)

    def run(self):
        """运行设置管理

        Returns:
            dict: 设置参数字典
        """
        self.migration_file()
        # 如果文件存在则读取,否则创建新文件
        return self.read() if self.path.is_file() else self.create()

    def read(self) -> dict:
        """读取设置文件

        Returns:
            dict: 读取的设置参数字典
        """
        # 读取设置文件
        with self.path.open("r", encoding=self.encode) as f:
            return self.compatible(load(f))

    def create(self) -> dict:
        """创建新的设置文件

        Returns:
            dict: 默认设置参数字典
        """
        # 创建新的设置文件
        with self.path.open("w", encoding=self.encode) as f:
            dump(self.default, f, indent=4, ensure_ascii=False)
        
        # 同时创建说明文档
        readme_path = self.path.parent / "settings_readme.md"
        if not readme_path.exists():
            with readme_path.open("w", encoding="utf-8") as f:
                f.write(self.readme_content)
                
        return self.default

    def update(self, data: dict):
        """更新设置文件内容

        Args:
            data: 要更新的设置参数字典
        """
        # 更新设置文件
        with self.path.open("w", encoding=self.encode) as f:
            dump(data, f, indent=4, ensure_ascii=False)

    def compatible(
        self,
        data: dict,
    ) -> dict:
        """兼容性检查,确保所有默认配置都存在

        Args:
            data: 要检查的设置参数字典

        Returns:
            dict: 经过兼容性检查后的设置参数字典
        """
        # 兼容性检查: 确保所有默认配置都存在
        update = False
        for i, j in self.default.items():
            if i not in data:
                data[i] = j
                update = True
        if update:
            self.update(data)
        return data

    def migration_file(self):
        """迁移设置文件

        如果旧的设置文件存在且新路径下不存在,则移动旧文件到新路径
        """
        if (
            old := self.root.parent.joinpath(self.name)
        ).exists() and not self.path.exists():
            move(old, self.path)
