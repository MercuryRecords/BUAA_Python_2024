# 一、功能简介

本项目实现了一个名为 **「Liberal Shared Platform」** 的共享练习平台，支持学生们在其中进行自由的练习、讨论和分享问题。

1. 多身份多用户系统：可以分别以用户和管理员的身份进行注册、登录、个人信息管理，并实现了用户认证。以用户身份参与到练习当中为平台主要功能，管理员身份处于顶层对用户、用户组、问题、问题组进行管理，两种身份间相互独立。
2. （用户）个人信息功能：用户可以自行执行注册、登录、登出、修改密码、修改头像等操作。
3. （用户）用户组功能：用户可以创建、搜索、加入、退出用户组，用户组的创建者还可以踢出成员或解散用户组。
4. （用户）题目功能：用户可以自行创建、更新、删除题目，并使用在线的OCR功能进行辅助题目的（批量）上传；用户可以在简洁的做题界面进行作答并提交，答题完成后可以查看做题情况并在题目对应讨论区进行讨论。
5. （用户）题单功能：用户可以自行创建、更新、删除题单，并将题单公开或分享到指定的用户组并设置权限。
6. （用户）错题记录功能：系统会自动记录用户的错题及做错时间，方便用户进行有目的的重复练习。
7. （用户）标签功能：用户可以在权限范围内编辑题目和题单的标签，并利用其进行筛选和对应的能力分析。
8. （用户）能力值系统：用户做完练习后，可以选择需要的单位查看个人练习的能力值，并且可以查看自己最擅长的标签和最薄弱的标签，使用户了解个人情况，针对性地进行练习。
9. （管理员）系统管理功能：管理员可以对用户账户进行统一的管理，包括注册、注销等功能；管理员同时对用户组、题目、题单等具有最高的管理编辑权限。
10. （管理员）敏感词屏蔽功能：管理员可以上传、删除敏感词，系统会自动对用户上传的所有问题字段进行检查，并将检查出的敏感词进行替换。

# 二、已完成任务

## （一）必做任务完成情况（完成 7 / 总数 7）

1. 用户和管理员注册、登录和个人信息管理。	
2. 用户可以选择创建和加入用户组，用户可以搜索和加入用户组。
3. 自动识别PDF或图片中的文本。识别后，可以编辑提取的文本结果以完成问题的输入。
4. 设计自己的或利用现有的数据结构，根据章节或其他标准将问题组织成类别。在解决问题时，用户可以选择一组特定的问题来处理。
5. 用户可以选择与特定组共享一组问题，也可以将其提供给所有人。共享问题的接收者可以访问问题组。
6. 搜索应具有可自定义的参数，但搜索范围应包括共享问题组和用户上传的问题。它不应该搜索尚未共享的问题组。
7. 根据用户的错误答案、错误频率以及用户指定的主题和问题数量，参考相关的推荐算法，生成一组问题，用户应使用您选择的科学有效的算法优先重新解决这些问题。

## （二）选做任务完成情况（完成 7 / 总数 2）

1. 系统可以筛选敏感词并将其从题库中删除。
2. 根据错误答案的类型和时间，参考相关材料，确定从学生错误问题信息到学生能力信息的转换标准。绘制一张图表，显示学生能力随时间的变化。
3. 使用标签系统对问题和问题组进行标记，并支持在上传或修改题目时生成推荐标签。<font color=red>（自定义）</font>
4. 为用户设计了头像系统，支持默认头像和上传修改头像。<font color=red>（自定义）</font>
5. 为题目设计了讨论区系统，支持用户对题目以及其他评论进行评论。<font color=red>（自定义）</font>
6. 为管理员设计了后台管理系统，支持对用户、用户组、题目、题目组进行顶层的管理。<font color=red>（自定义）</font>
7. 在用户和管理员的基本框架下增加了用户验证机制，使得【待填写】<font color=red>（自定义）</font>


# 三、总体设计方案

总体而言我们采用了前后端分离的方式进行开发，提高了开发效率和系统的可维护性。前端使用【待填写】，后端使用 Django 作为主体框架，结合ORM框架高效地管理数据库。核心代码围绕用户认证、权限管理、数据模型等构建，实现了功能的同时保证了代码的可读性和可扩展性。

## 基本架构

就前后端基本交互逻辑而言，我们极大程度地使用了MTV模型：

- M：Model，负责与数据库的交互。
- T：Template，负责展示数据。
- V：View，负责接收请求、调用Model和Template。

在本项目中，一个比较完整的交互流程大概如下：

```markdown
前端发出请求 ==> 视图函数进行响应，利用 ORM 框架进行数据库操作 ==> 反馈结果给前端
```

基本的交互流程就是这样，如非特殊功能，不再对 CRUD 操作进行详细说明。

## 1. 多用户多群组系统

### 1.1 功能设计

在这个多用户系统中，我们细致地划分了用户和管理员的不同权限与功能，以确保平台的顺利运行与高效管理。用户能够选择创建、加入、退出用户组等操作，而管理员则能全面监控平台状况，进行必要的调整与优化。

### 1.2 功能实现

就实现而言，对于数据库的 CRUD 操作，我们使用了 Django ORM 框架，通过定义模型类，可以方便地进行数据库的增删改查操作。在数据库中我们使用了自定义的模型，没有继承 Django 内置的用户模型。

```python
# backend/database/models.py
from django.db import models


class User(models.Model):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.png')
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)


class Manager(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=200, blank=True)
    members = models.ManyToManyField(User, related_name='groups')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    created_at = models.DateTimeField(auto_now_add=True)
```

在用户验证方面我们使用了自定义中间件进行实现。

```python
# backend/middleware/auth.py
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


class Authentication(MiddlewareMixin):
    def process_request(self, request):
        # 允许访问头像
        if request.method == "GET" and request.path_info.startswith(r"/media/avatars/"):
            return

        # 不检查一些路径
        if request.path_info in ['/api/user_register', '/api/user_login', '/api/user_register/', '/api/user_login/']:
            return

        register_name = request.session.get("username")
        user_name = request.POST.get("username")

        if not register_name or register_name != user_name:
            return JsonResponse({"code": 400, "message": "请先登录"})

        is_admin = request.session.get("usertype") == '0'
        is_admin_path = request.path_info.startswith('/api/admin_')

        if is_admin_path and not is_admin:
            return JsonResponse({"code": 400, "message": "普通用户无权限访问管理员接口"})

        if not is_admin_path and is_admin:
            return JsonResponse({"code": 400, "message": "管理员用户不应访问普通用户接口"})

```


## 2. 题目与题单系统

### 2.1 功能设计

我们设计了题目与题单系统，以便用户能够创建、更新和删除问题及题单。用户可以在线上传题目及题单，并使用OCR功能和推荐标签功能辅助完成题目的上传和编辑。在简洁的做题界面上，用户能进行作答并查看答题情况，同时在题目的讨论区里进行互动。管理员则能对这些内容进行高效的管理。

### 2.2 基础功能

在数据库中，我们定义了题目和题单的模型，并使用 Django ORM 进行数据库操作。

```python
# backend/database/models.py
from django.db import models

class ProblemGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_problem_groups')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200, blank=True)
    tags = models.ManyToManyField(Tag, related_name='problem_groups')
    problem_num = models.IntegerField(default=0)


class Problem(models.Model):
    problem_group = models.ForeignKey(ProblemGroup, on_delete=models.CASCADE, related_name="problems")
    index = models.IntegerField()
    type = models.CharField(max_length=1)  # 'c'(choice)选择题，'b'(blank)填空题
    title = models.CharField(max_length=30)  # 题目，默认情况下需要截取
    content = models.TextField(max_length=1000)  # 题干
    # ...

class ProblemPermission(models.Model):
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE, related_name="permissions")  # 用户群组
    problem_group = models.ForeignKey(ProblemGroup, on_delete=models.CASCADE, related_name="permissions")  # 问题群组
    permission = models.SmallIntegerField()  # 权限，0 仅可查看，1 可查看并添加问题
```

### 2.3 题单权限与分享功能

我们实现了题单的权限控制，包括私有、公开和分享给特定用户。用户可以创建私有题单，只有创建者可以查看和编辑。公开题单可以被所有用户查看，但只有创建者可以编辑。分享题单则允许特定用户查看和编辑。

在数据库中，我们定义了题单权限的模型，并在相关的视图函数中进行了权限控制。

# TODO: 补充示例代码，说明相关的视图函数

### 2.4 题目讨论区功能

我们实现了题目讨论区功能，用户可以在题目下方发表评论，并查看其他用户的评论。

在数据库中，我们定义了评论的模型，并在相关的视图函数中进行了评论的增删改查操作。

```python
# backend/database/views_comment.py

@require_http_methods(["POST"])
def comment_add(request):
    username = request.POST.get("username")
    user = User.objects.get(username=username)
    if not user:
        return E_USER_NOT_FIND

    parent_id = request.POST.get("parent_id")
    is_sub_comment = request.POST.get("is_sub_comment") == "y"
    content = request.POST.get("content")

    Comment.objects.create(user=user, parent_id=parent_id, content=content, is_sub_comment=is_sub_comment)

    return success("评论成功")
```

### 2.5 错题记录和标签功能

为了让用户在做题时能更好地掌握自己的学习情况，我们实现了错题记录和标签功能。用户可以查看自己的错题记录，并给题目添加标签以便于分类和查找。

在数据库中，我们定义了错题记录和标签的模型，并在相关的视图函数中进行了错题记录和标签的增删改查操作。

```python
# backend/database/models.py

class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    result = models.BooleanField(default=False)  # 是否正确
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=200, blank=True)
```

### 2.6 筛选搜索功能

# TODO

### 2.7 辅助功能

对本项目使用的 OCR 和 KeyBERT 进行详细说明：

为了辅助用户上传题目，我们使用了 OCR 技术来识别图片中的文字。我们使用了 Paddle 的 PaddleOCR，可以识别多种语言的文字，包括中文、英文等。OCR 技术可以帮助用户快速地将图片中的文字转换为可编辑的文本，从而提高题目上传的效率。PaddleOCR 识别的结果中还包括了置信度和位置信息，可以用于后续的文本处理。

```python
ocr_model = PaddleOCR(lang="ch", use_angle_cls=True, use_gpu=True)
```

为了进一步方便用户上传题目，我们使用了一种简单的基于规则的题目内容和选项提取功能，并将其用于 OCR 的结果中。该功能可以自动识别题目和选项，并将它们提取出来，方便用户进行编辑和修改。由于规则设计的比较简单，因此该功能可能无法处理一些复杂的题目，但可以满足大部分情况下上传多道选择题的需求。

```python
patterns = []
for char in 'ABCDEFGabcdefg':
    for left in '(（':
        for right in '）)':
            patterns.append(left + char + right)

for char in 'ABCDEFGabcdefg':
    patterns.append(char + '.')


def is_choice(text):
    for pat in patterns:
        if pat in text:
            return True
    return False


def text_split_to_questions(text):
    questions = []
    content = ""
    choices = []
    processing_content = True

    for i in range(len(text)):
        if "扫描全能王" in text[i]:
            continue

        if not is_choice(text[i]) and not processing_content:
            ques = {"content": content,
                    "choices": choices}

            content = ""
            choices = []
            questions.append(ques)

        processing_content = not is_choice(text[i])

        if processing_content:
            if content == "":
                content += text[i]
            else:
                content += "____" + text[i]
        else:
            choices.append(text[i])

    return questions
```

为了方便用户对题目进行分类和查找，我们参考了 KeyBERT 的实现思想，使用 BERT 模型对题目进行编码，尝试从题目和已有标签中找到最相似的标签，并向用户进行推荐。我们设置了一个阈值，只有相似度大于该阈值的标签才会被推荐给用户。该功能可以帮助用户更好地对题目进行分类和查找，提高题目的上传效率和用户体验。

```python
# KeyBERT 初始化
def tokenize_zh(text):
    words = jieba.lcut(text)
    return words


vectorizer = CountVectorizer(tokenizer=tokenize_zh)
st_model = SentenceTransformer(f'{settings.BASE_DIR}/model_path/paraphrase-multilingual-MiniLM-L12-v2')
kw_model = KeyBERT(model=st_model)

def _extract_keywords(text):
    text_embedding = st_model.encode(text, convert_to_tensor=True).reshape(1, -1)
    keywords = kw_model.extract_keywords(text, vectorizer=vectorizer)

    tags = [tag.name for tag in Tag.objects.all()]
    if tags:
        tags_embeddings = st_model.encode(tags, convert_to_tensor=True)

        similarities = cosine_similarity(text_embedding, tags_embeddings)
        tag_similarity_list = [(tag, sim) for tag, sim in zip(tags, similarities.tolist()[0])]
        keywords += tag_similarity_list

    keywords = [keyword for keyword in keywords if keyword[1] > 0.4]
    return keywords
```

## 3. 能力值系统

### 3.1 功能设计

能力值系统是本项目的一个核心功能，它可以帮助用户了解自己在不同学科和知识点上的掌握程度，从而更好地进行学习规划。能力值系统通过【待填写】

# TODO

### 3.2 代码实现/公式说明

## 4. 敏感词系统

### 4.1 功能设计

敏感词系统是本项目的一个辅助功能，它可以避免用户上传含有敏感信息的题目，从而保证系统的内容安全。敏感词系统通过对用户上传的文本内容进行敏感词检测，如内容中包含敏感词，则系统会将其替换为星号。对管理员而言，敏感词系统可以方便地查看和管理敏感词，从而更好地维护系统的内容安全。如确实需要上传含有敏感信息的题目，管理员可以手动修改题目内容，保证题目表达意思的准确性。

### 4.2 代码实现

# TODO

