from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category, Tag
from django.utils import timezone
from django.contrib.auth.models import User


def create_category(name="life", description=''):  # 관습 null 이 아니라 '' 으로
    category, is_created = Category.objects.get_or_create(  # get or create는 이름이 life 인 것이 있으면 get을 하고 없으면 만들어서 가져와라
        name=name,
        description=description
    )

    category.slug = category.name.replace(' ', '-').replace('/', '')
    category.save()  # slug를 위한 코드

    return category


def create_post(title, content, author, category=None):
    blog_post = Post.objects.create(
        title=title,
        content=content,
        creaded=timezone.now(),
        author=author,
        category=category
    )
    return blog_post


def create_tag(name="some_tag"):
    tag, is_created = Tag.objects.get_or_create(
        name=name
    )
    tag.slug = tag.name.replace(' ', '-').replace('/', '')
    tag.save()

    return tag


# Create your tests here. ## test할 코드를 작성
class TestView(TestCase):  # 테스트 모듈 상속
    def setUp(self):
        self.client = Client()
        self.author_000 = User.objects.create_user(username="smith", password='nopassword')
        self.user_obama = User.objects.create_user(username="obama", password='nopassword')  # 사용자 추가

    def check_navbar(self, soup):
        navbar = soup.find('div', id="navbar")
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)

    def check_right_side(self, body):
        # category card 에서
        category_card = body.find('div', id='category-card')
        self.assertIn('미분류(1)', category_card.text)  #### 미분류(1) 있어야 함
        self.assertIn('정치/사회(1)', category_card.text)  #### 정치/사회 (1) 있어야 함

    def test_post_list(self):  # 이 함수를 실행시킬 때 마다 새롭게 시작한다.
        response = self.client.get('/blog/')  # 숫자를 써주야만 해당 포스트로 간다.
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        # print(title) # <title>Title</title>
        self.assertEqual(title.text, ' - Blog')

        # navbar = soup.find('div', id = "navbar") # div 태크중에서 id가 navbar인 것을 찾는다.
        # # print(navbar.text)
        # self.assertIn("Blog", navbar.text) # navbar에 Blog가 있나?
        # self.assertIn("About me", navbar.text)

        self.assertEqual(Post.objects.count(), 0)  # Post.objects.count() Post에 게시글이 몇개인지 가져와라, 가져와서 0이면
        self.assertIn("아직 게시물이 없습니다.", soup.body.text)

        self.assertEqual(Post.objects.count(), 0)

        tag_america = create_tag(name='america')
        # post_000 = Post.objects.create(
        post_000 = create_post(
            title="The first post",
            content="Hello World We are thr world.",
            author=self.author_000
        )  # db 추가
        post_001 = create_post(
            title='The second post',
            content='Second Second Second',
            author=self.author_000,
            category=create_category(name='정치/사회')
        )
        ## 생성은 항상 앞에 있어야만 작동됨!!

        post_000.tags.add(tag_america)
        post_000.save()

        self.assertGreater(Post.objects.count(), 0)  # a가 b보다 크지 않는다. / 새로 DB를 만들고 그곳에서 테스트하기 때문에 fail

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)  # 접속 가능한지
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.body
        self.assertNotIn("아직 게시물이 없습니다.", body.text)
        self.assertIn(post_000.title, body.text)

        post_000_read_more_btn = body.find('a', id='read-more-post-{}'.format(post_000.pk))
        self.assertEqual(post_000_read_more_btn['href'], post_000.get_absolute_url())

        self.check_right_side(body)

        #### 첫번째 포스트에는 '정치/사회' 있어야 함
        main_div = body.find('div', id="main-div")
        self.assertIn('정치/사회', main_div.text)
        self.assertIn('미분류', main_div.text)

        # Tag
        post_card_000 = main_div.find('div', id='post-card-{}'.format(post_000.pk))
        self.assertIn("#america", post_card_000.text)  # tag가 해당 post의 card마다 있다.

    def test_post_list_by_category(self):
        category_politics = create_category(name='정치/사회')

        post_000 = create_post(
            title="The first post",
            content="Hello World We are thr world.",
            author=self.author_000,
        )  # db 추가

        post_001 = create_post(
            title='The second post',
            content='Second Second Second',
            author=self.author_000,
            category=create_category(name='정치/사회')
        )

        response = self.client.get(category_politics.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        # self.assertEqual('Blog - {}'.format(category_politics.name))

        main_div = soup.find('div', id='main-div')
        self.assertNotIn('미분류', main_div.text)
        self.assertIn('정치/사회', main_div.text)

    def test_post_detail(self):  #
        category_politics = create_category(name='정치/사회')

        post_000 = create_post(
            title="The first post",
            content="Hello World We are thr world.",
            author=self.author_000,
            category=category_politics
        )  # db 추가
        post_001 = create_post(
            title='The second post',
            content='Second Second Second',
            author=self.author_000
        )

        tag_america = create_tag(name="america")
        post_000.tags.add(tag_america)
        post_000.save()

        self.assertGreater(Post.objects.count(), 0)
        post_000_url = post_000.get_absolute_url()
        self.assertEqual(post_000.get_absolute_url(), '/blog/{}/'.format(post_000.pk))

        response = self.client.get(post_000_url)  # 숫자를 써주야만 해당 포스트로 간다.
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        # print(title.text)  #
        # self.assertEqual(title.text, '{} - Blog'.format(post_000.title))  # Title == Title  ?
        # 알수 없는 에러 발생으로 넘어감 강의시간 11:00
        self.check_navbar(soup)  # 네비게이션 바가 있니?

        body = soup.body
        main_div = body.find('div', id="main-div")
        self.assertIn(post_000.title, main_div.text)
        self.assertIn(post_000.author.username, main_div.text)
        self.assertIn(post_000.content, main_div.text)

        self.check_right_side(body)

        # Tag
        self.assertIn("#america", main_div.text)  # tag가 해당 post의 card마다 있다.

        self.assertIn(category_politics.name, main_div.text)  # category 가 main_div에 있다.
        # self.assertNotIn("EDIT", main_div.text) # EDIT 버튼이 로그인 하지 않은 경우 보이지 않는다.

        login_success = self.client.login(username="smith", password='nopassword')  # login을 한 경우에는
        self.assertTrue(login_success)
        response = self.client.get(post_000_url)  # F5
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find("div", id="main-div")

        self.assertEqual(post_000.author, self.author_000)  # post.author와 login한 사람이 사용자가 동일하면
        self.assertIn("EDIT", main_div.text)  # EDIT버튼이 있다.

        # 다른 사람일 경우는 EDIT 버튼이 없다.
        login_success = self.client.login(username="obama", password='nopassword')  # login을 한 경우에는
        self.assertTrue(login_success)
        response = self.client.get(post_000_url)  # F5
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find("div", id="main-div")
        self.assertNotEqual(post_000.author, self.user_obama)  # post.author와 login한 사람이 사용자가 동일하면
        self.assertNotIn("EDIT", main_div.text)  # EDIT버튼이 있다.

    def test_post_list_no_category(self):
        category_politics = create_category(name='정치/사회')
        post_000 = create_post(
            title="The first post",
            content="Hello World We are thr world.",
            author=self.author_000,
        )  # db 추가
        post_001 = create_post(
            title='The second post',
            content='Second Second Second',
            author=self.author_000,
            category=create_category(name='정치/사회')
        )

        response = self.client.get('/blog/category/_none/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        # self.assertEqual('Blog - {}'.format(category_politics.name))

        main_div = soup.find('div', id='main-div')
        self.assertIn('미분류', main_div.text)
        self.assertNotIn('정치/사회', main_div.text)


class TestModel(TestCase):
    def setUp(self):
        self.client = Client()
        self.author_000 = User.objects.create_user(username="smith", password='nopassword') # create가 아닌 creat_user 필수!!

    def test_category(self):
        category = create_category()

        post_000 = create_post(
            title="The first post",
            content="Hello World We are thr world.",
            author=self.author_000,
            category=category  # 카테고리를 만들어서 넣기
        )  # db 추가

        self.assertEqual(category.post_set.count(), 1)  # 해당 category의 포스트의 갯수가 1이 맞냐??

    def test_tag(self):
        tag_000 = create_tag(name='bad_guy')
        tag_001 = create_tag(name='america')
        post_000 = create_post(
            title="The first post",
            content="Hello World We are thr world.",
            author=self.author_000,
        )  # db 추가
        post_001 = create_post(
            title="Stay Fool, Stay Hungry",
            content="Hello World We are thr world.",
            author=self.author_000,
        )  # db 추가
        post_000.tags.add(tag_000)
        post_000.tags.add(tag_001)
        post_000.save()

        post_001.tags.add(tag_001)
        post_001.save()

        self.assertEqual(post_000.tags.count(), 2)  # post는 여러개의 tag를 가질 수 있다.
        self.assertEqual(tag_001.post_set.count(), 2)  # 하나의 tag는 여러개의 post에 붙을 수 있다.
        self.assertEqual(tag_001.post_set.first(), post_000)  # 하나의 tag는 자신을 가진 post들을 불러올 수 있다.
        self.assertEqual(tag_001.post_set.last(), post_001)  # 하나의 tag는 자신을 가진 post들을 불러올 수 있다.

    def test_post(self):
        category = create_category()

        post_000 = create_post(
            title="The first post",
            content="Hello World We are thr world.",
            author=self.author_000,
            category=category  # 카테고리를 만들어서 넣기
        )  # db 추가

    def test_tag_page(self):
        tag_000 = create_tag(name='bad_guy')
        tag_001 = create_tag(name='america')
        post_000 = create_post(
            title="The first post",
            content="Hello World We are thr world.",
            author=self.author_000,
        )  # db 추가
        post_001 = create_post(
            title="Stay Fool, Stay Hungry",
            content="Hello World We are thr world.",
            author=self.author_000,
        )  # db 추가
        post_000.tags.add(tag_000)
        post_000.tags.add(tag_001)
        post_000.save()

        post_001.tags.add(tag_001)
        post_001.save()

        response = self.client.get(tag_000.get_absolute_url())

        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        main_div = soup.find('div', id="main-div")
        blog_div = main_div('h1', id="blog-list-title")
        self.assertIn("#{}".format(tag_000.name), main_div.text)
        self.assertIn(post_000.title, main_div.text)
        self.assertNotIn(post_001.title, main_div.text)

    def test_post_create(self):
        response = self.client.get('/blog/create/')  # 문제없지 접근이 되는지 확인 models에 get_update_url 추가
        self.assertNotEqual(response.status_code, 200)
        self.client.login(username="smith", password='nopassword')
        response = self.client.get('/blog/create/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', id="main-div")


    def test_post_update(self):
        post_000 = create_post(
            title="The first post",
            content="Hello World We are thr world.",
            author=self.author_000,
        )  # db 추가

        self.assertEqual(post_000.get_update_url(), post_000.get_absolute_url() + "update/")

        response = self.client.get(post_000.get_update_url())  # 문제없지 접근이 되는지 확인 models에 get_update_url 추가
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_div = soup.find('div', id = "main-div")

        self.assertNotIn('creaded', main_div.text)
        self.assertNotIn('Author', main_div.text)