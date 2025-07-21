from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import pymysql
from datetime import datetime
import json
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 文件上传配置
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'zzn20041031',  # 请修改为您的数据库密码
    'database': 'smartscreen',
    'charset': 'utf8mb4' 
}

def get_db_connection():
    """获取数据库连接"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def format_response(success=True, message="", data=None):
    """统一响应格式"""
    return jsonify({
        "success": success,
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/')
def index():
    return render_template('index.html')



# ==================== 消息通知接口 ====================

@app.route('/api/announcements', methods=['GET'])
def get_announcements():
    """获取消息通知列表"""
    try:
        connection = get_db_connection()
        if not connection:
            return format_response(False, "数据库连接失败")
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 获取查询参数
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        type_filter = request.args.get('type')
        is_important = request.args.get('is_important')
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if type_filter:
            where_conditions.append("type = %s")
            params.append(type_filter)
        
        if is_important is not None:
            where_conditions.append("is_important = %s")
            params.append(1 if is_important.lower() == 'true' else 0)
        
        where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 查询总数
        count_sql = f"SELECT COUNT(*) as total FROM announcements{where_clause}"
        cursor.execute(count_sql, params)
        total = cursor.fetchone()['total']
        
        # 查询数据
        offset = (page - 1) * limit
        data_sql = f"""
            SELECT id, title, content, author_name, type, is_important, created_at 
            FROM announcements{where_clause} 
            ORDER BY is_important DESC, created_at DESC 
            LIMIT %s OFFSET %s
        """
        cursor.execute(data_sql, params + [limit, offset])
        announcements = cursor.fetchall()
        
        # 格式化时间
        for announcement in announcements:
            announcement['created_at'] = announcement['created_at'].isoformat()
        
        result = {
            "list": announcements,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
        
        return format_response(True, "获取成功", result)
        
    except Exception as e:
        return format_response(False, f"获取失败: {str(e)}")
    finally:
        if connection:
            connection.close()

@app.route('/api/announcements', methods=['POST'])
def create_announcement():
    """创建消息通知"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['title', 'content', 'type']
        for field in required_fields:
            if not data.get(field):
                return format_response(False, f"缺少必填字段: {field}")
        
        connection = get_db_connection()
        if not connection:
            return format_response(False, "数据库连接失败")
        
        cursor = connection.cursor()
        
        sql = """
            INSERT INTO announcements (title, content, author_name, type, is_important)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (
            data['title'],
            data['content'],
            data.get('author_name', '系统管理员'),
            data['type'],
            data.get('is_important', 0)
        ))
        
        connection.commit()
        announcement_id = cursor.lastrowid
        
        return format_response(True, "创建成功", {"id": announcement_id})
        
    except Exception as e:
        return format_response(False, f"创建失败: {str(e)}")
    finally:
        if connection:
            connection.close()

@app.route('/api/announcements/<int:announcement_id>', methods=['PUT'])
def update_announcement(announcement_id):
    """更新消息通知"""
    try:
        data = request.get_json()
        
        connection = get_db_connection()
        if not connection:
            return format_response(False, "数据库连接失败")
        
        cursor = connection.cursor()
        
        # 检查记录是否存在
        cursor.execute("SELECT id FROM announcements WHERE id = %s", (announcement_id,))
        if not cursor.fetchone():
            return format_response(False, "通知不存在")
        
        # 构建更新字段
        update_fields = []
        params = []
        
        for field in ['title', 'content', 'author_name', 'type', 'is_important']:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if not update_fields:
            return format_response(False, "没有要更新的字段")
        
        sql = f"UPDATE announcements SET {', '.join(update_fields)} WHERE id = %s"
        params.append(announcement_id)
        
        cursor.execute(sql, params)
        connection.commit()
        
        return format_response(True, "更新成功")
        
    except Exception as e:
        return format_response(False, f"更新失败: {str(e)}")
    finally:
        if connection:
            connection.close()

@app.route('/api/announcements/<int:announcement_id>', methods=['DELETE'])
def delete_announcement(announcement_id):
    """删除消息通知"""
    try:
        connection = get_db_connection()
        if not connection:
            return format_response(False, "数据库连接失败")
        
        cursor = connection.cursor()
        
        # 检查记录是否存在
        cursor.execute("SELECT id FROM announcements WHERE id = %s", (announcement_id,))
        if not cursor.fetchone():
            return format_response(False, "通知不存在")
        
        cursor.execute("DELETE FROM announcements WHERE id = %s", (announcement_id,))
        connection.commit()
        
        return format_response(True, "删除成功")
        
    except Exception as e:
        return format_response(False, f"删除失败: {str(e)}")
    finally:
        if connection:
            connection.close()

# ==================== 文件上传接口 ====================

@app.route('/api/upload/image', methods=['POST'])
def upload_image():
    """上传图片文件"""
    try:
        # 检查是否有文件
        if 'image' not in request.files:
            return format_response(False, "没有选择文件")
        
        file = request.files['image']
        
        # 检查文件名
        if file.filename == '':
            return format_response(False, "没有选择文件")
        
        # 检查文件类型
        if not allowed_file(file.filename):
            return format_response(False, "不支持的文件类型，请上传图片文件")
        
        # 生成唯一文件名
        filename = secure_filename(file.filename)
        
        # 安全地获取文件扩展名
        if '.' in filename:
            file_extension = filename.rsplit('.', 1)[1].lower()
        else:
            # 如果没有扩展名，默认使用 jpg
            file_extension = 'jpg'
        
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # 保存文件
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # 生成访问URL
        file_url = f"/uploads/{unique_filename}"
        
        return format_response(True, "上传成功", {
            "filename": unique_filename,
            "url": file_url,
            "original_name": filename
        })
        
    except Exception as e:
        return format_response(False, f"上传失败: {str(e)}")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """提供上传文件的访问"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ==================== 实验室优秀项目接口 ====================

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """获取项目列表"""
    try:
        connection = get_db_connection()
        if not connection:
            return format_response(False, "数据库连接失败")
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        # 获取查询参数
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        achievement_type = request.args.get('achievement_type')
        
        # 构建查询条件
        where_conditions = []
        params = []
        
        if achievement_type:
            where_conditions.append("achievement_type = %s")
            params.append(achievement_type)
        
        where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
        
        # 查询总数
        count_sql = f"SELECT COUNT(*) as total FROM projects{where_clause}"
        cursor.execute(count_sql, params)
        total = cursor.fetchone()['total']
        
        # 查询项目数据
        offset = (page - 1) * limit
        data_sql = f"""
            SELECT id, project_name, description, achievement_type, achievement_details, 
                   start_date, end_date, image_url
            FROM projects{where_clause} 
            ORDER BY end_date DESC 
            LIMIT %s OFFSET %s
        """
        cursor.execute(data_sql, params + [limit, offset])
        projects = cursor.fetchall()
        
        # 为每个项目获取成员信息
        for project in projects:
            # 格式化日期
            if project['start_date']:
                project['start_date'] = project['start_date'].isoformat()
            if project['end_date']:
                project['end_date'] = project['end_date'].isoformat()
            
            # 获取项目成员
            member_sql = """
                SELECT u.id, u.full_name, pm.role_in_project
                FROM project_members pm
                JOIN users u ON pm.user_id = u.id
                WHERE pm.project_id = %s
                ORDER BY pm.role_in_project
            """
            cursor.execute(member_sql, (project['id'],))
            project['members'] = cursor.fetchall()
        
        result = {
            "list": projects,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
        
        return format_response(True, "获取成功", result)
        
    except Exception as e:
        return format_response(False, f"获取失败: {str(e)}")
    finally:
        if connection:
            connection.close()

@app.route('/api/projects', methods=['POST'])
def create_project():
    """创建项目"""
    connection = None
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['project_name', 'achievement_type']
        for field in required_fields:
            if not data.get(field):
                return format_response(False, f"缺少必填字段: {field}")
        
        connection = get_db_connection()
        if not connection:
            return format_response(False, "数据库连接失败")
        
        cursor = connection.cursor()
        
        # 插入项目基本信息
        sql = """
            INSERT INTO projects (project_name, description, achievement_type, 
                                achievement_details, start_date, end_date, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (
            data['project_name'],
            data.get('description'),
            data['achievement_type'],
            data.get('achievement_details'),
            data.get('start_date'),
            data.get('end_date'),
            data.get('image_url')
        ))
        
        project_id = cursor.lastrowid
        
        # 添加项目成员
        if 'members' in data and data['members']:
            member_sql = "INSERT INTO project_members (project_id, user_id, role_in_project) VALUES (%s, %s, %s)"
            for member in data['members']:
                cursor.execute(member_sql, (
                    project_id,
                    member['user_id'],
                    member.get('role_in_project', '组员')
                ))
        
        connection.commit()
        
        return format_response(True, "创建成功", {"id": project_id})
        
    except Exception as e:
        if connection:
            connection.rollback()
        return format_response(False, f"创建失败: {str(e)}")
    finally:
        if connection:
            connection.close()

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """更新项目"""
    connection = None
    try:
        data = request.get_json()
        
        connection = get_db_connection()
        if not connection:
            return format_response(False, "数据库连接失败")
        
        cursor = connection.cursor()
        
        # 检查项目是否存在
        cursor.execute("SELECT id FROM projects WHERE id = %s", (project_id,))
        if not cursor.fetchone():
            return format_response(False, "项目不存在")
        
        # 更新项目基本信息
        update_fields = []
        params = []
        
        for field in ['project_name', 'description', 'achievement_type', 'achievement_details', 
                     'start_date', 'end_date', 'image_url']:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if update_fields:
            sql = f"UPDATE projects SET {', '.join(update_fields)} WHERE id = %s"
            params.append(project_id)
            cursor.execute(sql, params)
        
        # 更新项目成员
        if 'members' in data:
            # 删除原有成员
            cursor.execute("DELETE FROM project_members WHERE project_id = %s", (project_id,))
            
            # 添加新成员
            if data['members']:
                member_sql = "INSERT INTO project_members (project_id, user_id, role_in_project) VALUES (%s, %s, %s)"
                for member in data['members']:
                    cursor.execute(member_sql, (
                        project_id,
                        member['user_id'],
                        member.get('role_in_project', '组员')
                    ))
        
        connection.commit()
        
        return format_response(True, "更新成功")
        
    except Exception as e:
        if connection:
            connection.rollback()
        return format_response(False, f"更新失败: {str(e)}")
    finally:
        if connection:
            connection.close()

@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """删除项目"""
    try:
        connection = get_db_connection()
        if not connection:
            return format_response(False, "数据库连接失败")
        
        cursor = connection.cursor()
        
        # 检查项目是否存在
        cursor.execute("SELECT id FROM projects WHERE id = %s", (project_id,))
        if not cursor.fetchone():
            return format_response(False, "项目不存在")
        
        # 删除项目（成员会因为外键约束自动删除）
        cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))
        connection.commit()
        
        return format_response(True, "删除成功")
        
    except Exception as e:
        return format_response(False, f"删除失败: {str(e)}")
    finally:
        if connection:
            connection.close()

# ==================== 辅助接口 ====================

@app.route('/api/users', methods=['GET'])
def get_users():
    """获取用户列表（用于项目成员选择）"""
    try:
        connection = get_db_connection()
        if not connection:
            return format_response(False, "数据库连接失败")
        
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        
        sql = "SELECT id, username, full_name FROM users ORDER BY full_name"
        cursor.execute(sql)
        users = cursor.fetchall()
        
        return format_response(True, "获取成功", users)
        
    except Exception as e:
        return format_response(False, f"获取失败: {str(e)}")
    finally:
        if connection:
            connection.close()

@app.route('/api')
def api_info():
    """API信息"""
    return jsonify({
        "message": "智能电子班牌后端API",
        "version": "1.0.0",
        "endpoints": {
            "announcements": "/api/announcements",
            "projects": "/api/projects",
            "users": "/api/users"
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
  