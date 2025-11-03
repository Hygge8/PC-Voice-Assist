# CI/CD 配置说明

本项目使用 GitHub Actions 实现持续集成和持续部署(CI/CD),确保代码质量和项目稳定性。

## 工作流概览

项目配置了以下 GitHub Actions 工作流:

### 1. CI 工作流 (ci.yml)

主要的持续集成工作流,在每次推送和 Pull Request 时自动运行。

**触发条件**:
- 推送到 `main` 或 `develop` 分支
- 针对 `main` 或 `develop` 分支的 Pull Request

**包含的任务**:

#### 测试任务 (test)

在多个操作系统和 Python 版本上运行测试,确保跨平台兼容性。

**测试矩阵**:
- 操作系统: Ubuntu, macOS, Windows
- Python 版本: 3.11, 3.12

**执行步骤**:
1. 检出代码
2. 设置 Python 环境(使用 pip 缓存加速)
3. 安装系统依赖(portaudio, espeak 等)
4. 安装 Python 依赖
5. 使用 flake8 进行代码检查
6. 运行 pytest 测试并生成覆盖率报告
7. 上传覆盖率报告到 Codecov

#### 代码质量检查 (code-quality)

检查代码格式和质量标准。

**检查项目**:
- **black**: 代码格式化检查
- **isort**: 导入语句排序检查
- **mypy**: 类型检查
- **pylint**: 代码质量检查

#### 安全扫描 (security)

扫描代码和依赖中的安全漏洞。

**扫描工具**:
- **safety**: 检查依赖包的已知安全漏洞
- **bandit**: Python 代码安全扫描

扫描结果会上传为构建产物,可以在 Actions 页面下载查看。

### 2. 依赖审查工作流 (dependency-review.yml)

在 Pull Request 时审查依赖变更,检测潜在的安全风险。

**功能**:
- 检测新增或更新的依赖
- 评估依赖的安全风险
- 在 PR 中自动添加审查摘要
- 如果发现中等或更高严重级别的漏洞,构建失败

### 3. CodeQL 分析工作流 (codeql.yml)

使用 GitHub 的 CodeQL 进行深度代码安全分析。

**触发条件**:
- 推送到 `main` 或 `develop` 分支
- 针对 `main` 分支的 Pull Request
- 每周一定时运行

**分析内容**:
- 安全漏洞检测
- 代码质量问题
- 最佳实践违规

分析结果会显示在仓库的 Security 标签页。

### 4. 发布工作流 (release.yml)

在创建版本标签时自动创建 GitHub Release。

**触发条件**:
- 推送格式为 `v*.*.*` 的标签(如 v1.0.0)

**执行步骤**:
1. 从 CHANGELOG.md 提取版本更新日志
2. 创建 GitHub Release
3. 构建 Python 包
4. 上传构建产物

### 5. 文档检查工作流 (docs.yml)

检查文档质量和完整性。

**检查项目**:
- **Markdown Lint**: 检查 Markdown 文件格式
- **Link Check**: 检查文档中的链接是否有效
- **Spell Check**: 拼写检查

## 配置文件说明

### pyproject.toml

项目的主要配置文件,包含:

**项目元数据**:
- 项目名称、版本、描述
- 作者信息
- 依赖列表
- 项目 URL

**工具配置**:
- **black**: 代码格式化配置(行长度 100)
- **isort**: 导入排序配置
- **pytest**: 测试配置
- **coverage**: 覆盖率配置
- **mypy**: 类型检查配置
- **pylint**: 代码检查配置

### .flake8

Flake8 代码检查工具的配置:
- 最大行长度: 100
- 排除目录: .git, __pycache__, venv 等
- 忽略的规则: E203, E501, W503

### .codecov.yml

Codecov 覆盖率报告配置:
- 项目覆盖率目标: 自动
- 阈值: 5%
- 忽略: tests/, examples/, docs/

### .github/markdown-link-check-config.json

Markdown 链接检查配置:
- 超时时间: 20 秒
- 重试次数: 3 次
- 忽略本地链接和某些特殊链接

## 使用指南

### 本地运行检查

在提交代码前,可以在本地运行这些检查:

#### 安装开发依赖

```bash
pip install -r requirements.txt
pip install pytest pytest-cov black isort flake8 mypy pylint
```

#### 代码格式化

```bash
# 检查格式
black --check .
isort --check .

# 自动格式化
black .
isort .
```

#### 代码检查

```bash
# Flake8 检查
flake8 .

# Pylint 检查
pylint src/

# MyPy 类型检查
mypy src/ --ignore-missing-imports
```

#### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行测试并生成覆盖率报告
pytest tests/ -v --cov=src --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

#### 安全扫描

```bash
# 安装工具
pip install safety bandit

# 检查依赖安全
safety check

# 代码安全扫描
bandit -r src/
```

### 查看 CI 结果

1. 访问仓库的 **Actions** 标签页
2. 选择相应的工作流运行
3. 查看各个任务的执行结果
4. 如果失败,点击任务查看详细日志

### 处理 CI 失败

#### 测试失败

1. 查看失败的测试用例
2. 在本地复现问题
3. 修复代码并重新测试
4. 推送修复

#### 代码格式问题

```bash
# 自动修复格式问题
black .
isort .
```

#### 类型检查问题

根据 mypy 的提示添加类型注解或使用 `# type: ignore` 注释。

#### 安全问题

1. 查看 safety 或 bandit 的报告
2. 更新有漏洞的依赖
3. 修复代码中的安全问题

### 创建发布

1. 更新 CHANGELOG.md,添加新版本的更新内容
2. 创建并推送版本标签:

```bash
git tag v1.0.0
git push origin v1.0.0
```

3. GitHub Actions 会自动创建 Release

## 徽章

可以在 README.md 中添加以下徽章显示 CI 状态:

```markdown
![CI](https://github.com/Hygge8/PC-Voice-Assist/workflows/CI/badge.svg)
![CodeQL](https://github.com/Hygge8/PC-Voice-Assist/workflows/CodeQL%20Analysis/badge.svg)
[![codecov](https://codecov.io/gh/Hygge8/PC-Voice-Assist/branch/main/graph/badge.svg)](https://codecov.io/gh/Hygge8/PC-Voice-Assist)
```

## 最佳实践

### 提交前检查

在提交代码前,建议运行:

```bash
# 格式化代码
black .
isort .

# 运行测试
pytest tests/ -v

# 代码检查
flake8 .
```

### Pull Request

1. 确保所有 CI 检查通过
2. 检查代码覆盖率是否下降
3. 查看依赖审查结果
4. 确保没有引入新的安全问题

### 版本发布

1. 在 `develop` 分支开发新功能
2. 合并到 `main` 分支
3. 更新 CHANGELOG.md
4. 创建版本标签
5. 检查自动创建的 Release

## 故障排除

### CI 运行缓慢

- 检查是否有不必要的依赖安装
- 使用缓存加速依赖安装
- 考虑并行运行独立的任务

### 测试在 CI 中失败但本地通过

- 检查环境差异(操作系统、Python 版本)
- 确保测试不依赖本地文件或配置
- 使用相同的 Python 版本进行测试

### 覆盖率上传失败

- 检查 Codecov token 是否配置
- 确保覆盖率文件生成正确
- 查看 Codecov 的错误日志

## 进一步改进

可以考虑添加的功能:

- **性能测试**: 添加性能基准测试
- **集成测试**: 添加端到端集成测试
- **自动部署**: 自动部署到测试环境
- **通知**: 在 CI 失败时发送通知
- **代码审查机器人**: 自动审查代码质量

## 参考资源

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [pytest 文档](https://docs.pytest.org/)
- [black 文档](https://black.readthedocs.io/)
- [Codecov 文档](https://docs.codecov.io/)
- [CodeQL 文档](https://codeql.github.com/docs/)

