async function sendEditorData() {
    const editorData = {
        username: "test_user",
        age: 25
    };

    const response = await fetch("http://127.0.0.1:8000/editor", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(editorData)
    });

    const result = await response.json();
    console.log(result);
}

sendEditorData();
