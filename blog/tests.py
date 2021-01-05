from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
from django.utils import timezone
from django.contrib.auth.models import User

# Create your tests here. ## test할 코드를 작성
class TestView(TestCase) : # 테스트 모듈 상속
    def setUp(self):
        self.client = Client()
        self.author_000 = User.objects.create(username="smith", password='nopassword')


    def test_post_list(self): # 이 함수를 실행시킬 때 마다 새롭게 시작한다.
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        print(title) # <title>Title</title>
        self.assertEqual(title.text, 'Title') # Title == Title  ?

        navbar = soup.find('div', id = "navbar") # div 태크중에서 id가 navbar인 것을 찾는다.
        print(navbar.text)
        self.assertIn("Blog", navbar.text) # navbar에 Blog가 있나?
        self.assertIn("About me", navbar.text)

        self.assertEqual(Post.objects.count(), 0) # Post.objects.count() Post에 게시글이 몇개인지 가져와라, 가져와서 0이면
        self.assertIn("아직 게시물이 없습니다.", soup.body.text)

        self.assertEqual(Post.objects.count(), 0)

        post_000 = Post.objects.create(
            title = "The first post",
            content="Hello World We are thr world.",
            creaded = timezone.now(),
            author = self.author_000,
        ) # db 추가
        self.assertGreater(Post.objects.count(), 0) # a가 b보다 크지 않는다. / 새로 DB를 만들고 그곳에서 테스트하기 때문에 fail

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200) # 접속 가능한지
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.body
        self.assertNotIn("아직 게시물이 없습니다.", body.text)
        self.assertIn(post_000.title , body.text)

    def test_post_detail(self):
        pass