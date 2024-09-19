2024 夏季学期 Python 全英课程大作业，报告文档见 report.md

## TODO

请设计一个平台，学生可以上传和共享问题。学生应该能够在这个平台上测试自己。

- 问题应该包括多种格式，如多选和填空。自行获取问题。
- 界面应该美观，但不要过于花哨，以免分散解决问题的注意力。可以添加其他功能，但它们应该易于使用且用户友好。
- 基本要求：用户和管理员注册、登录和个人信息管理。
- 用户群组：用户可以创建和加入组，用户可以搜索和加入组。
- 上传：识别PDF或图片中的文本自动。识别后，提取的文本结果可以编辑以完成问题输入。提示：使用OCR。
- 问题分组：设计自己的或利用现有数据结构将问题分类为章节或其他标准。解决问题时，用户可以选择特定题单进行工作。问题解决界面应该根据个人偏好进行设计，避免过多要求。
- 问题共享：用户可以选择将题单共享给特定组或所有人。共享问题的接收者可以访问题单。
- 搜索组：搜索应该具有自定义参数，但搜索范围应该包括共享题单和用户上传的问题。不要搜索未共享的题单。
- 错误日志：根据用户错误答案、错误频率和指定科目及问题数量，利用相关推荐算法生成一套用户应该优先重新解决的问题。
- 系统负责筛选敏感词汇并将其从问题库中删除。找到实现此功能的方法。
- 可视化学生能力。根据错误答案的类型和时间，参考相关材料并定义一个转换标准，将学生的错误问题信息转换为学生能力信息。创建一个显示学生能力随时间变化的图。
- 根据需要实现其他功能，根据实用性和工作量获得额外分数。

