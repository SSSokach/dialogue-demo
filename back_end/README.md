# dialogue demo backend

>  A Django project

## 运行方式

- django原生

```bash
python ../manage.py runserver 127.0.0.1:8067
```

- uwsgi （支持多线程）

```bash
# 启动
uwsgi --ini video_demo_uwsgi.ini 

# 结束
killall -s INT /home/long/miniconda3/envs/py37mme2e/bin/uwsgi

# 查看
ps aux|grep uwsgi
```

