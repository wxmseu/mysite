from django.utils.safestring import mark_safe
import copy
"""
自定义的分页组件，使用说明：
在视图函数中：
def pretty_num_list(request):

    # 1. 根据自己的情况，筛选数据，确定queryset
    queryset = models.PrettyNumber.objects.filter(**dic).order_by('id')  # '-'表示倒序
    
    # 2. 实例化分页对象
    page_obj = Pagination(request, queryset)
    
    content = {
        "query_set": page_obj.page_queryset,         # 分完页的对象
        "search_data": search_data,         
        "page_str": page_obj.html()                  # 生成页码
    }
    return render(request, 'pretty_num_list.html', content)

在前端页面：
    {% for item in query_set %}
        {{ item.xx}}
    {% endfor %}


    <ul class="pagination">
            {{ page_str }}
    </ul>

"""


class Pagination(object):
    def __init__(self, request, queryset, page_parm="page", pagesize=10, plus=5):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据
        :param page_parm: 在URL中传递的获取分页的参数，例如/pretty_num/list/?page=21
        :param pagesize: 每页显示多少条数据
        :param plus: 显示当前页的前后几页
        """
        query_dict=copy.deepcopy(request.GET)
        query_dict._mutable=True
        self.query_dict=query_dict
        self.page_parm=page_parm
        page = request.GET.get(page_parm, '1')
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.pagesize = pagesize
        self.plus = plus
        self.start = (self.page - 1) * self.pagesize
        self.end = self.page * self.pagesize
        self.page_queryset = queryset[self.start:self.end]
        self.request = request

        total_count = queryset.count()
        total_pages, div = divmod(total_count, self.pagesize)
        if div:
            total_pages += 1
        self.total_pages = total_pages

    def html(self):

        # 计算出显示 当前页码的前plus页和后plus页
        if self.total_pages < 2 * self.plus + 1:
            # 数据库中的数据比较少的情况
            start_page = 1
            end_page = self.total_pages
        else:
            # 数据库比较多的情况下

            # 当前页<plus的情况
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus
            else:
                # 当前页+plus>total_pages
                if self.page + self.plus > self.total_pages:
                    start_page = self.total_pages - 2 * self.plus
                    end_page = self.total_pages
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []
        # 首页
        self.query_dict.setlist(self.page_parm,[1])
        first_page = "<li><a href='?{}'>首页</a></li>".format(self.query_dict.urlencode())
        page_str_list.append(first_page)
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_parm, [self.page - 1])
            prev = "<li><a href='?{}'>上一页</a></li>".format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_parm, [1])
            prev = "<li><a href='?{}'>上一页</a></li>".format(self.query_dict.urlencode())
        page_str_list.append(prev)
        # 中间页
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_parm, [i])
            if i == self.page:
                ele = "<li class='active'><a href='?{}'>{}</a></li>".format(self.query_dict.urlencode(), i)
            else:
                ele = "<li><a href='?{}'>{}</a></li>".format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        # 下一页
        if self.page < self.total_pages:
            self.query_dict.setlist(self.page_parm, [self.page + 1])
            next_page = "<li><a href='?{}'>下一页</a></li>".format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_parm, [self.total_pages])
            next_page = "<li><a href='?{}'>下一页</a></li>".format(self.query_dict.urlencode())
        page_str_list.append(next_page)
        # 尾页
        self.query_dict.setlist(self.page_parm, [self.total_pages])
        last_page = "<li><a href='?{}'>尾页</a></li>".format(self.query_dict.urlencode())
        page_str_list.append(last_page)
        # 跳转页面框
        search_str = """
            <li>
                <form method="get" style="float: left;margin-left: -1px">
                    <div class="input-group" style="width: 150px">
                        <input name="page"
                               style="position: relative;float: left;display: inline-block;width: 88px;border-radius: 0"
                               type="text" class="form-control"  placeholder="页码">
                        <span class="input-group-btn">
                            <button class="btn btn-default" type="submit">跳转</button>
                        </span>
                    </div>
                </form>
            </li>
            """
        page_str_list.append(search_str)
        page_str = mark_safe("".join(page_str_list))
        return page_str
