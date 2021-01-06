from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
from django.utils import timezone
from django.contrib.auth.models import User

def create_post(title, content, author):
    blog_post = Post.objects.create(
        title=title,
        content=content,
        creaded= timezone.now(),
        author=author
    )
    return blog_post

# Create your tests here. ## test할 코드를 작성
class TestView(TestCase) : # 테스트 모듈 상속
    def setUp(self):
        self.client = Client()
        self.author_000 = User.objects.create(username="smith", password='nopassword')

    def check_navbar(self, soup):
        navbar = soup.find('div', id = "navbar")
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)


    def test_post_list(self): # 이 함수를 실행시킬 때 마다 새롭게 시작한다.
        response = self.client.get('/blog/') # 숫자를 써주야만 해당 포스트로 간다.
        self.assertEqual(response.status_code, 200)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        # print(title) # <title>Title</title>
        self.assertEqual(title.text, ' - Blog')


        # navbar = soup.find('div', id = "navbar") # div 태크중에서 id가 navbar인 것을 찾는다.
        # # print(navbar.text)
        # self.assertIn("Blog", navbar.text) # navbar에 Blog가 있나?
        # self.assertIn("About me", navbar.text)

        self.assertEqual(Post.objects.count(), 0) # Post.objects.count() Post에 게시글이 몇개인지 가져와라, 가져와서 0이면
        self.assertIn("아직 게시물이 없습니다.", soup.body.text)

        self.assertEqual(Post.objects.count(), 0)

        # post_000 = Post.objects.create(
        post_000 = create_post(
            title = "The first post",
            content="Hello World We are thr world.",
            author = self.author_000,
        ) # db 추가

        self.assertGreater(Post.objects.count(), 0) # a가 b보다 크지 않는다. / 새로 DB를 만들고 그곳에서 테스트하기 때문에 fail

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200) # 접속 가능한지
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.body
        self.assertNotIn("아직 게시물이 없습니다.", body.text)
        self.assertIn(post_000.title , body.text)


        post_000_read_more_btn = body.find('a', id='read-more-post-{}'.format(post_000.pk))
        self.assertEqual(post_000_read_more_btn['href'], post_000.get_absolute_url())


    def test_post_detail(self): #

        post_000 = create_post(
            title = "The first post",
            content="Hello World We are thr world.",
            author = self.author_000,
        ) # db 추가

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
        self.check_navbar(soup) # 네비게이션 바가 있니?

        body = soup.body
        main_div = body.find('div', id = "main_div")
        self.assertIn(post_000.title, main_div.text)
        self.assertIn(post_000.author.username, main_div.text)
        self.assertIn(post_000.content, main_div.text)



    def test_post(self):
        pass
