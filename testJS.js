async function loginData(){
  const response = await fetch("http://127.0.0.1:8000/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "application/json"
    },
    credentials: "include",
    body: new URLSearchParams({
      email: "defario777@mail.ru",
      password: "rfvtljp14"
    }),
  });

  if (!response.ok) {
    console.error("Ошибка при входе:", response.status, await response.text());
    return;
  }

  const data = await response.json();
  console.log("Успешный вход:", data);
}

async function getMe() {
  const response = await fetch("http://127.0.0.1:8000/users/me", {
    method: "GET",
    credentials: "include",
    headers: {
      "Accept": "application/json"
    }
  });
  if (!response.ok) {
    console.error("Ошибка получения профиля:", response.status, await response.text());
    return;
  }

  const data = await response.json();
  console.log("Текущий пользователь:", data);
}

async function main() {
  await loginData();
  await getMe();
}

main();

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
