import subprocess

from mysite.celery import app


@app.task()
def get_task():
    return 'task...'


@app.task()
def async_crawl_smzdm():
    """定时运行 Scrapy 爬取什么值得的买商品评论"""
    r = subprocess.run('cd ../smzdm;python run.py;',
                       shell=True,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)

    with open('./log/smzdm.log', 'a') as f_out, open('./log/smzdm.err', 'a') as f_err:
        f_out.write(r.stdout.decode('utf-8'))
        f_err.write(r.stderr.decode('utf-8'))
    return 'success'
