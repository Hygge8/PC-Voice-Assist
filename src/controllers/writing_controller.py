"""
写作控制器
负责使用AI生成文章
"""
import os
from pathlib import Path
from datetime import datetime
from typing import Optional
from openai import OpenAI
import config


class WritingController:
    """写作控制器"""
    
    def __init__(self):
        """初始化写作控制器"""
        self.client = OpenAI()
        self.model = config.OPENAI_MODEL
    
    def write_article(self, topic: str, length: str = "medium", save_path: Optional[str] = None) -> str:
        """
        写一篇文章
        
        Args:
            topic: 文章主题
            length: 文章长度 (short/medium/long)
            save_path: 保存路径
            
        Returns:
            执行结果描述
        """
        try:
            # 获取长度描述
            length_desc = config.ARTICLE_LENGTHS.get(length, config.ARTICLE_LENGTHS["medium"])
            
            # 构建提示词
            prompt = f"""请写一篇关于"{topic}"的文章。

要求:
- 文章长度: {length_desc}
- 结构清晰,包含引言、正文和结论
- 语言流畅,内容专业
- 使用Markdown格式

请直接输出文章内容,不要有其他说明。"""
            
            print(f"正在生成文章: {topic}...")
            
            # 调用大模型生成文章
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的文章写作助手,擅长撰写各类主题的高质量文章。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            article_content = response.choices[0].message.content
            
            # 确定保存路径
            if not save_path:
                # 生成默认文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{topic}_{timestamp}.md"
                save_path = os.path.join(config.DEFAULT_ARTICLE_DIR, filename)
            
            # 确保目录存在
            save_dir = Path(save_path).parent
            save_dir.mkdir(parents=True, exist_ok=True)
            
            # 保存文章
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(f"# {topic}\n\n")
                f.write(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
                f.write(article_content)
            
            return f"文章已生成并保存到: {save_path}\n文章长度: 约{len(article_content)}字"
            
        except Exception as e:
            return f"生成文章时出错: {str(e)}"

