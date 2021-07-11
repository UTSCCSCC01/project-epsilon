const Home = () => {
  return (
    <div>
      <div id="background" class="title-card">
          <h1>Epsilon</h1>
          <hr/>
      </div>
      <div class="contents">
          <form action="" method="post">
              <br/>
              <input class="btn" type="submit" value="Log out"/>
          </form>
      </div>
      <div>
          <p>
              Hello World! Welcome to Epsilon!
          </p>
          <h3>
              Here are the pages that are available:
          </h3>
          <ul>
              <li><a href="">this page</a></li>
              <li><a href="/login">login page</a></li>
              <li><a href="/registration">EP-1 team registration/create team page</a></li>
              <li><a href="/displayteam/1/">EP-2,4,5 Display team page</a></li>
              <li><a href="/jointeamrequest/1/">EP-3 Display pending join team request page</a></li>
              <li><a href="/user/1/">EP-20 Display user account info</a></li>
          </ul>
          <h3>
              Here are the pages for development.
          </h3>
          <ul>
              <li><a href="/create">create tables and populate with test data page</a></li>
              <li><a href="/deleteAll">drops all tables page</a></li>
          </ul>
      </div>
  </div>
  );
}

export default Home;
