async function loginData(){
    const response = fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      credentials: "include",
      body: new URLSearchParams({
        email: "test@example.com",
        password: "str1"
      }),
    })
    .then(response => response.json())
    .then(data => {
      console.log("Ответ от сервера:", data);
    })
    .catch(error => {
      console.error("Ошибка:", error);
    });
}

// loginData()

async function getMe() {
    const response = await fetch("http://127.0.0.1:8000/users/me", {
        method: "GET"
    })
    .then(response => response.json())
    .then(data => {
      console.log("Ответ от сервера:", data);
    })
    .catch(error => {
      console.error("Ошибка:", error);
    });
}

// getMe()

async function registration() {
    const email = "test12312312321@example.com"
    //const nickname = document.getElementById('nickname').value;
    const firstName = "STR"
    const lastName = "STR"
    const password = "str1"

    // Отправляем данные на сервер
    fetch("http://127.0.0.1:8000/users/create_user", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email: email,
            first_name: firstName,
            last_name: lastName,
            password: password
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Ответ от сервера:", data);
    })
    .catch(error => {
        console.error("Ошибка:", error);
    });
}

// registration()
