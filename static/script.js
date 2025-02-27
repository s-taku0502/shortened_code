document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("shorten-form");
    const resultDiv = document.getElementById("result");
    const shortUrlElem = document.getElementById("short-url");
    const copyBtn = document.getElementById("copy-btn");
    const shareBtn = document.getElementById("share-btn");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const urlInput = document.getElementById("original-url").value;

        const response = await fetch("/shorten", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: urlInput })
        });

        if (response.ok) {
            const data = await response.json();
            if (data.shortened_url) {
                shortUrlElem.textContent = data.shortened_url;
                shortUrlElem.href = data.shortened_url;
                resultDiv.style.display = "block";
            }
        } else {
            const errorData = await response.json();
            alert(`エラー: ${errorData.error || "不明なエラーが発生しました。"}`);
        }
    });

    copyBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(shortUrlElem.href).then(() => {
            alert("リンクをコピーしました！");
        }).catch(err => {
            console.error("コピーに失敗しました: ", err);
        });
    });

    shareBtn.addEventListener("click", () => {
        if (navigator.share) {
            navigator.share({
                title: "短縮URL",
                url: shortUrlElem.href
            }).then(() => {
                console.log("共有成功");
            }).catch(err => {
                console.error("共有エラー: ", err);
            });
        } else {
            alert("このブラウザでは共有機能がサポートされていません。");
        }
    });
});
