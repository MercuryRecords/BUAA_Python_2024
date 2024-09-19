[//]: # (# 项目 DEMO：http://39.105.19.133:5173/)

# 一、功能简介

本项目实现了一个名为 **「Liberal Shared Platform」** 的共享练习平台，支持学生们在其中进行自由的练习、讨论和分享问题。

1. 多身份多用户系统：可以分别以用户和管理员的身份进行注册、登录、个人信息管理，并实现了用户认证。以用户身份参与到练习当中为平台主要功能，管理员身份处于顶层对用户、用户群组、问题、题单进行管理，两种身份间相互独立。
2. （用户）个人信息功能：用户可以自行执行注册、登录、登出、修改密码、修改头像等操作。
3. （用户）用户群组功能：用户可以创建、搜索、加入、退出用户群组，用户群组的创建者还可以踢出成员或解散用户群组。
4. （用户）题目功能：用户可以自行创建、更新、删除题目，并使用在线的OCR功能进行辅助题目的（批量）上传；用户可以在简洁的做题界面进行作答并提交，答题完成后可以查看做题情况并在题目对应讨论区进行讨论。
5. （用户）题单功能：用户可以自行创建、更新、删除题单，并将题单公开或分享到指定的用户群组并设置权限。
6. （用户）错题记录功能：系统会自动记录用户的错题及做错时间，方便用户进行有目的的重复练习。
7. （用户）标签功能：用户可以在权限范围内编辑题目和题单的标签，并利用其进行筛选和对应的能力分析。
8. （用户）能力值系统：用户做完练习后，可以选择需要的单位查看个人练习的能力值，并且可以查看自己最擅长的标签和最薄弱的标签，使用户了解个人情况，针对性地进行练习。
9. （管理员）系统管理功能：管理员可以对用户账户进行统一的管理，包括注册、注销等功能；管理员同时对用户群组、题目、题单等具有最高的管理编辑权限。
10. （管理员）敏感词屏蔽功能：管理员可以上传、删除敏感词，系统会自动对用户上传的所有问题字段进行检查，并将检查出的敏感词进行替换。

# 二、已完成任务

## （一）必做任务完成情况（完成 7 / 总数 7）

1. 用户和管理员注册、登录和个人信息管理。	
2. 用户可以选择创建和加入用户群组，用户可以搜索和加入用户群组。
3. 自动识别PDF或图片中的文本。识别后，可以编辑提取的文本结果以完成问题的输入。
4. 设计自己的或利用现有的数据结构，根据章节或其他标准将题单织成类别。在解决问题时，用户可以选择一组特定的问题来处理。
5. 用户可以选择与特定组共享一组问题，也可以将其提供给所有人。共享问题的接收者可以访问题单。
6. 搜索应具有可自定义的参数，但搜索范围应包括共享题单和用户上传的问题。它不应该搜索尚未共享的题单。
7. 根据用户的错误答案、错误频率以及用户指定的主题和问题数量，参考相关的推荐算法，生成一组问题，用户应使用您选择的科学有效的算法优先重新解决这些问题。

## （二）选做任务完成情况（完成 7 / 总数 2）

1. 系统可以筛选敏感词并将其从题库中删除。
2. 根据错误答案的类型和时间，参考相关材料，确定从学生错误问题信息到学生能力信息的转换标准。绘制一张图表，显示学生能力随时间的变化。
3. 使用标签系统对问题和题单进行标记，并支持在上传或修改题目时生成推荐标签。<font color=red>（自定义）</font>
4. 为用户设计了头像系统，支持默认头像和上传修改头像。<font color=red>（自定义）</font>
5. 为题目设计了讨论区系统，支持用户对题目以及其他评论进行评论。<font color=red>（自定义）</font>
6. 为管理员设计了后台管理系统，支持对用户、用户群组、题目、题目组进行顶层的管理。<font color=red>（自定义）</font>
7. 在用户和管理员的基本框架下增加了用户验证机制，使用户仅可访问当前已登录用户拥有的资源，而不得通过特殊手段向服务器发出违规请求，以访问其它用户资源或假冒管理员更改系统数据。<font color=red>（自定义）</font>


# 三、总体设计方案

总体而言我们采用了前后端分离的方式进行开发，提高了开发效率和系统的可维护性。前端使用 Vue 作为主体框架，后端使用 Django 作为主体框架，结合 ORM 框架高效地管理数据库。核心代码围绕用户认证、权限管理、数据模型等构建，实现了功能的同时保证了代码的可读性和可扩展性。

## 基本架构

就前后端基本交互逻辑而言，我们极大程度地使用了 MTV 模型：

- M：Model，负责与数据库的交互。
- T：Template，负责展示数据。
- V：View，负责接收请求、调用 Model 和 Template。

在本项目中，一个比较完整的交互流程大概如下：

```markdown
前端发出请求 ==> 视图函数进行响应，利用 ORM 框架进行数据库操作 ==> 反馈结果给前端
```

基本的交互流程就是这样，如非特殊功能，不再对 CRUD 操作进行详细说明。

## 1. 多用户多群组系统

### 1.1 功能设计

在这个多用户系统中，我们细致地划分了用户和管理员的不同权限与功能，以确保平台的顺利运行与高效管理。用户能够选择创建、加入、退出用户群组等操作，而管理员则能全面监控平台状况，进行必要的调整与优化。

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

        # 不检查无需用户验证的路径
        if request.path_info in ['/api/user_register', '/api/user_register/',
                                 '/api/user_login', '/api/user_login/',
                                 '/api/get_avatar', '/api/get_avatar/',
                                 '/api/user_logout', '/api/user_logout/']:
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

我们设计了题目与题单系统，以便用户能够创建、更新和删除问题及题单。用户可以在线上传题目及题单，并使用 OCR 功能和推荐标签功能辅助完成题目的上传和编辑。在简洁的做题界面上，用户能进行作答并查看答题情况，同时在题目的讨论区里进行互动。管理员则能对这些内容进行高效的管理。

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
```

### 2.3 题单权限与分享功能

我们实现了题单的权限控制，包括私有、公开分享和分享给特定群组。用户可以自行创建私有题单，此时默认只有创建者拥有此题单权限。用户可以选择仅查看、查看并编辑两种权限之一，将私有题单公开分享或分享给特定群组，此时分享的目标群组同样拥有此题单权限。但在任何情况下，只有题单创建者（或管理员）可以删除题单。

在数据库中，我们定义了题单权限的模型，并在相关的视图函数中进行了权限控制。

```python
# backend/database/models.py

class ProblemPermission(models.Model):
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE, related_name="permissions")  # 分享题单的目标群组，为空则表示公开分享
    problem_group = models.ForeignKey(ProblemGroup, on_delete=models.CASCADE, related_name="permissions")  # 被分享的题单
    permission = models.SmallIntegerField()  # 权限，0 仅可查看，1 可查看并修改
```
```python
# backend/database/views_problem.py

# 获取用户正在请求的题单，并检查权限
# 0 为仅查看权限，1 为修改权限，2 为删除权限（仅创建者有）
def _get_problem_group(request, permission):
    username = request.POST.get('username')
    problem_group_id = request.POST.get('problem_group_id')

    # 检查题单是否存在
    check = ProblemGroup.objects.filter(id=problem_group_id)
    if not check:
        return E_PROBLEM_GROUP_NOT_FIND
    problem_group = check[0]

    # 如果用户不是题单的创建者，则需要检查权限
    if username != problem_group.user.username:
        check = User.objects.filter(username=username)
        if not check:
            return E_USER_NOT_FIND
        user = check[0]

        # 检查用户是否有权限
        # 即该题单是否在 Permission 数据库中有被公开分享的记录
        # 或是否存在包含该用户的某个群组，在 Permission 数据库中有该题单被分享至该群组的记录
        groups = user.groups.all()
        if not ProblemPermission.objects.filter(group__isnull=True, problem_group=problem_group, permission__gte=permission).exists() and not ProblemPermission.objects.filter(group__in=groups, problem_group=problem_group, permission__gte=permission).exists():
            return E_PERMISSION_DENIED

    return problem_group
```
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

为了让用户清晰地查看、搜索自己可见的所有题单中的题目，故设置题库板块，用户访问时，首先在数据库中查找用户具有查看权限的全部题目供用户查看。用户还可以根据群组、标签等方式在题目中进行筛选，或根据题目中的关键字搜索题目，并点击解题按钮快速进入答题页面。
```python
# backend/database/views_problem.py

def _get_problem_groups_with_permissions__gte(user, group_name, permission):
    if group_name == '_created_by_self': # 筛选用户自行创建的题单
        problem_groups = ProblemGroup.objects.filter(user=user)
    else:
        if group_name == '_shared_to_all': # 筛选所有公开题单
            # 查找题单被公开分享的记录
            permissions = ProblemPermission.objects.filter(group__isnull=True, permission__gte=permission)
        elif group_name: # 筛选某个群组下的所有题单
            group = Group.objects.filter(name=group_name)
            if not group:
                return E_GROUP_NOT_FIND
            group = group[0]

            if not user in group.members.all():
                return E_USER_NOT_IN_GROUP
            # 查找题单被分享至该群组的记录
            permissions = ProblemPermission.objects.filter(group=group, permission__gte=permission)
        else: # 获取用户可见的全部题单
            # 获取用户所在的所有群组
            groups = user.groups.all()
            # 查找题单被公开分享的记录或被分享至 groups 中某个群组的记录
            query = Q(group__isnull=True) | Q(group__in=groups)
            permissions = ProblemPermission.objects.filter(query, permission__gte=permission)
        problem_group_ids = permissions.values_list('problem_group', flat=True)

        query = Q(id__in=problem_group_ids)
        if not group_name:
            query |= Q(user=user)

        problem_groups = ProblemGroup.objects.filter(query)

    return problem_groups

def _get_problems_with_permissions(user, group_name):
    # 获取用户可见的所有题单
    problem_groups = _get_problem_groups_with_permissions__gte(user, group_name, 0)
    if isinstance(problem_groups, JsonResponse):
        return problem_groups

    # 返回可见题单中的所有题
    problems = Problem.objects.filter(problem_group__in=problem_groups)
    return problems
```
为减少前后端过多的数据传输，题库界面具体题目的筛选与搜索由前端实现：即前端在从后端获得第一次筛选（用户群组筛选）的题目后，在当前的题目清单下使用`filter`进行对问题标题、id、创建者、群组名、内容、标签的筛选，最终呈现在界面上的数据是`filteredProblems.value`。
```vue
const onSearch = () => {
    filteredProblems.value = allProblems.value.filter(problem => {
        const matchKeyword = searchForm.keyword === '' ||
        problem.problem_title.includes(searchForm.keyword) ||
        problem.id === parseInt(searchForm.keyword) ||
        problem.creator.includes(searchForm.keyword) ||
        problem.problem_group_title.includes(searchForm.keyword) ||
        problem.content.includes(searchForm.keyword)
        const matchTags = searchForm.selectedTags.length === 0 ||
        searchForm.selectedTags.every(tag => problem.tags.includes(tag))
        return matchKeyword && matchTags
    })
    currentPage.value = 1
    ElMessage.success(`找到 ${total.value} 个匹配的题目`)
}
```

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

能力值系统是本项目的一个核心功能，它可以帮助用户了解自己在不同学科和知识点上的掌握程度，从而更好地进行学习规划。能力值系统通过用户最近的做题记录，为每位用户计算相应的能力值，并支持计算历史时刻的能力值，展示个人能力值在一段时间内的变化趋势。同时，能力值系统可以对每个不同的知识点标签，单独计算用户对于这一标签的能力值和薄弱指数，并从其中选择能力值最大的 5 个标签和薄弱指数最大的 5 个标签，作为用户最擅长的知识点标签和最薄弱的知识点标签展示。

### 3.2 概念阐释
#### 3.2.1 题目掌握度
对于每个题目，取最多近五次做题记录计算题目掌握度。具体地，定义 $w_i$ 为最近第 i 次做题记录的权重，设置 $w_1 = 10, w_2 = 8, w_3 = 4, w_4 = 2, w_5 = 1$。定义 $(correct_p)_i$ 为题目 p 最近第 i 次做题的情况，回答正确则 $(correct_p)_i = 1$，回答错误则 $(correct_p)_i = 0$。设 $master_p$ 为用户对题目 p 的掌握度，$n_p$ 为用户练习此题的总次数，则题目 p 的掌握度可用如下公式计算：
$$
 master_p = \dfrac{\sum_{1\leqslant i\leqslant min(5,n_p)} (correct_p)_i * w_i}{\sum_{1\leqslant i\leqslant min(5,n_p)} w_i}
$$
#### 3.2.2 题目难度系数
定义 $difficulty_p$ 为题目 p 的难度系数，$rate_p$ 为题目 p 在所有用户中的总体正确率，则有如下公式：
$$
difficulty_p = 1 + (1 - rate_p) * 9
$$
#### 3.2.3 能力值
定义 $capability$ 为当前用户能力值，则有
$$
capability = \sum_{用户做过的所有共享问题 p} master_p * difficulty_p
$$
同样，定义 $capability_t$ 为用户对知识点标签 t 的能力值，则有
$$
capability_t = \sum_{用户做过的所有具有标签 t 的共享问题 p} master_p * difficulty_p
$$
为了限制用户上传无意义的问题，并利用这些问题提高自己的能力值，我们规定用户自行上传的问题不在能力值计算的考虑范围之内，即用户必须做由他人上传并共享的题才可以提高自身能力值。这是在公式中对用户做过的所有共享问题求和，而非所有问题求和的原因。
#### 3.2.4 薄弱指数
定义题目 p 的相对简单程度 $easy_p = rate_p$，其中 $rate_p$ 为题目 p 在所有用户中的总体正确率。定义 $weakness_t$ 为用户对知识点标签 t 的薄弱指数，则有
$$
weakness_t = \dfrac{\sum_{用户做过的所有具有标签 t 的共享问题 p}(1 - master_p) * easy_p}{\sum_{用户做过的所有具有标签 t 的共享问题 p}easy_p}
$$
同样，我们规定用户自行上传的问题不在薄弱指数的计算范围之内。
### 3.3 代码实现
以计算能力值为例：
```python
# backend/database/views_assessment.py

# 获取用户在当前和前 during_num 个历史时刻的能力值
@require_http_methods(["POST"])
def get_ability_trace(request):
    user = User.objects.get(username=request.POST.get('username'))
    during_interval = int(request.POST.get('during_interval')) # 两个历史时刻之间的间隔秒数
    during_num = int(request.POST.get('during_num'))
    filter_tag = request.POST.get('filter_tag')
    current_time = int(time.time())

    if filter_tag:
        # 筛选所有包含 filter_tag 的问题
        tag = Tag.objects.filter(name=filter_tag)
        if not tag:
            return E_TAG_NOT_FIND
        problems = tag[0].problems.all()
        # 去除其中用户自行上传的问题
        problems = problems.exclude(creator=user)
    else:
        # 取所有问题中非用户自行上传的问题
        problems = Problem.objects.exclude(creator=user)
    
    # 根据问题获取当前用户的做题记录
    records = Record.objects.filter(user=user, problem__in=problems).order_by('-created_at')
    
    # 列表中的每个字典存放不同时刻之前的做题记录
    datas = [{} for _ in range(during_num)]
    for record in records:
        # 按时间倒序遍历每条做题记录
        record_time = (current_time - record.get_unix_timestamp()) // during_interval
        update_limit = min(record_time + 1, during_num)
        # 索引小于 update_limit 的字典，其表示的时刻在做题记录产生的时间之后，应该向其中加入本条做题记录
        # 索引大于等于 update_limit 的字典，其表示的时刻在做题记录产生的时间之前，不加入本条做题记录
        for i in range(0, update_limit):
            _update_dict(datas[i], record.problem.id, record.result)
    
    result = []
    for data in datas:
        # 将不同时刻之前的做题记录按公式转化为在对应时刻的能力值
        result.append(_calc_ability(data))

    return success_data("能力值获取成功", result[::-1])

```
## 4. 敏感词系统

### 4.1 功能设计

敏感词系统是本项目的一个辅助功能，它可以避免用户发布含有敏感信息的题目或评论，从而保证系统的内容安全。敏感词系统通过对用户上传的文本内容进行敏感词检测，如内容中包含敏感词，则系统会将其替换为星号。对管理员而言，可以在管理员界面查看和管理敏感词，从而更好地维护系统的内容安全。敏感词系统不会影响管理员上传的内容，如用户确实需要上传含有敏感信息的题目，管理员可以在用户上传题目后，手动将被屏蔽为“*”的敏感词改回原有内容，保证题目表达意思的准确性。

### 4.2 代码实现
为了方便地对用户上传的多处内容进行敏感词过滤，我们使用了 Django 的中间件功能，将敏感词系统作为 Django 的中间件实现。
```python
# backend/backend/middleware/sensitive_detection.py
from django.utils.deprecation import MiddlewareMixin
from database.models import SensitiveWord

import re

# 此处设置要屏蔽敏感词的接口和参数
sensitive_keys = {
    '/api/user_register': ['username'], # 用户名不能出现敏感词
    '/api/group_create': ['group_name', 'group_description'], # 群组名称和描述不能出现敏感词
    '/api/group_apply_to_join': ['apply_reason'],
    '/api/problem_group_create': ['title', 'description', 'tags[]'], # 题单名称和描述不能出现敏感词
    '/api/problem_group_update': ['title', 'description', 'tags[]'],
    '/api/problem_create': ['title', 'content', 'field1', 'field2', 'field3', 'field4', 'field5', 'field6', 'field7', 'tags[]'], # 题目中不能出现敏感词
    '/api/problem_update': ['title', 'content', 'field1', 'field2', 'field3', 'field4', 'field5', 'field6', 'field7', 'tags[]'],
    '/api/comment_add': ['content'], # 评论内容不能出现敏感词
}
sensitive_words = []
compiled_patterns = []
dirty_flag = True # 脏标记，只有当管理员增加/删除敏感词时，才重新从数据库中读取敏感词

# 将 text 中的敏感词替换为等长的 '*'
def _censor(text):
    def _replace_sensitive_content(match):
        return '*' * len(match.group(0))
    for pattern in compiled_patterns:
        text = pattern.sub(_replace_sensitive_content, text)
    return text

# 管理员增加/删除敏感词后调用此函数
def setflag():
    global dirty_flag
    dirty_flag = True

class SensitiveDetection(MiddlewareMixin):
    def process_request(self, request):
        request_path = request.path_info
        if request_path.endswith('/'):
            request_path = request_path[:-1]
        
        for path in sensitive_keys.keys():
            if path == request_path:
                keys = sensitive_keys[path]
                # 开始准备敏感词过滤
                global sensitive_words, compiled_patterns, dirty_flag
                if dirty_flag:
                    # 从数据库重新读取敏感词
                    sensitive_words = SensitiveWord.objects.values_list('content', flat=True)
                    # 支持敏感词为正则表达式
                    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in sensitive_words]
                    dirty_flag = False
                
                request.POST._mutable = True # 允许修改请求内容

                for key in keys:
                    if key in request.POST:
                        # 为同时兼容参数为单值和列表的情况，使用 getlist / setlist
                        content_list = request.POST.getlist(key)
                        new_content_list = [_censor(s) for s in content_list]
                        request.POST.setlist(key, new_content_list)
                
                request.POST._mutable = False
                break

```
# 四、项目运行过程
## Django 配置流程
- 安装 MySQL 数据库，建议为 8.4.0 版本。
- 修改 backend/backend/settings.py 的 DATABASE 配置，将 PASSWORD 修改为数据库 root 用户的密码，其余键值使用默认即可。
- 使用命令行 `mysql -u root -p` 进入 MySQL 数据库，运行 `CREATE DATABASE mysql_demo` 建立项目数据库。
- 在项目根目录使用命令行 `mysql -u root -p mysql_demo < database_sample.sql` 导入项目示例数据库，**或者**在项目 backend 目录下依次使用命令行 `python manage.py makemigrations` 和 `python manage.py migrate` 初始化空的数据库。
- 在项目 backend 目录下使用命令行 `python manage.py runserver` 启动服务。 
## Vue 配置流程

前端依赖安装：

```powershell
cd frontend
npm install
```

安装完毕后可以执行：

```powershell
npm run dev
```

点击 `Local` 处超链接即可访问。
## 服务器配置流程
推荐访问已配置好的 demo：http://39.105.19.133:5173/

如果希望模拟项目在服务器上运行（例如将个人电脑临时作为局域网服务器），可参考以下步骤。

- 在 frontend/package.json 加入本机在局域网中的 IP 地址，如：
```json
  "scripts": {
    "dev": "vite --host 192.168.137.1",
    "build": "run-p type-check \"build-only {@}\" --",
    "preview": "vite preview",
    "build-only": "vite build",
    "type-check": "vue-tsc --build --force"
  }
```
- 在 frontend/src/plugins/axios.ts 中，将 baseURL 更改为本机 IP 地址的 8000 端口，如：
```Typescript
const API = axios.create({
    timeout: 500000,
    headers: {'X-Requested-With': 'XMLHttpRequest'},
    baseURL: 'http://192.168.137.1:8000/api/',
    withCredentials : true
})
```
- 在项目 backend 目录下运行  `python manage.py runserver {本机 IP 地址的 8000 端口}`，如：
```powershell
python manage.py runserver 192.168.137.1:8000
```

- 在项目 frontend 目录下运行 `npm run dev`。
# 五、项目总结

总体上来说，我们认为我们的项目完成情况还不错。大作业给出的基础功能和选做功能我们均以实现。在大作业发表后，我们就迅速确定了前后端的分工，并计划采用 Django+Vue 的前后端进行项目开发。负责后端的同学针对性地去学习 Django、MySQL，负责前端的同学先后学习了 html、css、JavaScript，然后学习了 Vue3 相关知识。因为是做题平台，所以说我们的风格是追求简约舒适沉浸，在满足功能的情况下尽可能使其好看。

从项目开始到项目结束，我们的过程进行得有条不紊。在开始之前，我们进行了一次正式的讨论会议，并用 Markdown 记录下了接下来具体要完成的任务。工作流程上，后端先写好具体接口，然后编写接口文档，前端只需要浏览接口文档通过调用 axios 库便可以轻松与后端进行通信。可以说前端与后端的配合是相当好的。此外，当遇到问题时，我们会及时在微信群进行交流，前端向后端提出需求，后端负责实现。当做完功能时，我们都会进行测试来保证功能的正确性。整个项目开发过程中，我们高度遵循 git 规范，这使得我们的代码维护十分轻松，所以我们的代码是具有高维护性和可扩展性的。



# 六、课程学习收获

## 1.**课程收获**和**难点分析**（小组成员是否有Python或大作业要求的基础，做完这个大作业自我感觉是否有提高等其他收获，本次项目感觉最困难的地方在哪里）

课程收获：

小组成员基本都有一定的 Python 基础，但是没有大作业要求的基础。通过这次的暑期课程学习，一方面对 Python 的基础语法知识、Python GUI 的理解提高了许多，另一方面在完成大作业的过程中，我们先后学习了 Django、Vue，对前后端交流协作有了更多认识。因为是第一次接触项目的开发，所以有很多无法自我解决的地方需要上网检索办法，在搜索方法中提高了我们对于信息的获取能力。

困难点：

首先是前端的页面设计，因为是大作业前才决定采用现代化框架 Vue3 进行开发，之前又没有页面设计的经验，所以对于我们想要做一个什么样的页面并不清晰。最终我们是采用了现有的轮子 elementUI plus 进行了构建。

其次是 css 样式的调整，这是一个无底洞，页面的设计好不好看基本都来自于 css 的作用。像处理对齐，居中，当很多零件组合在一起的时候，调整便变得相当困难。

对于后端使用的 Django 框架，由于初次接触后端开发，一切都需要从头学起，有网络教程的部分相对容易，但还有很多在开发过程中需要不断查资料自己摸索的东西。比如由于采用了前后端分离的开发模式，Django 的 session 机制在一开始完全不起作用，导致用户验证功能无法正常进行。在设计数据库的时候，我也困惑于如何设计出尽可能高效的数据结构，如何进行数据库搜索效率更高。然而由于经验的缺乏，在设计时还是优先考虑了实现的复杂程度和正确性，对效率的追求并没有被充分考虑，这也是今后可以努力的方向之一。

## 2.**教师授课评价**（老师上课过程的一些建议，以及希望老师之后能够介绍一些什么东西）

老师上课讲的非常细致且全面，面面俱到，未接触过 Python 课程的同学能够快速入门并提高自己的能力，有过基础的同学也能够从老师的授课中学到更多知识。暂无对老师授课的建议。

## 3.助教评价

助教十分负责热心，会在群里及时解答同学们的疑惑，在同学们做题遇到困难的时候，会及时给出提示以帮助我们解题。

## 4.**当前课程教授内容评价与**课程进一步改进建议

课程进度以及教授内容安排合理。从一开始的基础打印语句入门，慢慢提高难度，让学习过程循序渐进。并且最后讲授了 Python GUI，为大作业提供了帮助。平时的作业巩固了我们在课堂上学到的知识，大作业则锻炼了我们的自主学习能力，信息检阅能力，分工合作能力，对项目开发有了一个初步的了解，是一门非常不错的课程。

平时的小作业中有些填空题的指向还不是很明确，用词偶尔会出现歧义，因此我们建议之后能注意题目的用词，以助同学们不被混淆。



## 七、主要参考资料
[手把手教你（web+Django+vue开发实战）学完可就业](https://www.bilibili.com/video/BV1kK411o7z3)
[尚硅谷Vue3入门到实战，最新版vue3+TypeScript前端开发教程_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Za4y1r7KE/?spm_id_from=333.337.search-card.all.click)
