## payhere assignment
### 실행: 
```
1. git clone this repository
2. pip install -r requirements.txt
3. ddl.sql 파일로 table 생성
4. uvicorn src.main:app --port 8000 --reload 명령어로 fastapi app 실행
5. 로컬 환경에서 test 가정 시, 인터넷 url에 http://localhost:8000/docs를 실행,
   fastapi swagger docs 화면에서 api를 test한다
```

### Api Test 방법:
```
ledger 관련 api들은 접근 제한 처리가 되어 있어, 
signup, login을 먼저 한 후 token을 생성해야 이용이 가능하다

signup을 했거나, login을 하여 jwt token을 생성하고
fastapi docs 우측 상단의 Authorize 탭을 클릭,
value안에 생성된 토큰을 입력하면 ledger api들을 사용할 수 있다

토큰 유효 시간은 30분이다.

로그아웃을 원한다면, Authorize 탭의 logout을 사용한다.

```

### 참고사항:
```
1. .env 파일의 db 정보
   (username, password, localhost, db name, port)들은
   test 하는 환경에 맞춰서 수정할 것
   (개발 시에는 docker로 local 환경에 mysql 생성하여 test하였음)

2. ddl.sql 파일 하단의 dml insert 구문들은, 테스트 용으로 미리 생성한 것으로
   UserLogin 을 먼저 insert 한 후, Ledger insert를 실행할 것
   (test 시, 새

3. 로그아웃 기능은, blacklist 방식으로 유효하지 않은 jwt 토큰을 
   따로 저장하는 logic을 구현하는 것이 많은 설계가 필요하여
   fastapi docs 화면의 우측 상단 Authorize 탭의 logout으로 대체하였음

4. 가계부 세부 내역 공유를 위한 복제, 특정 시간 후 만료되는 단축 url 생성은 
   구현하지 않았음

```

