// import Request from "./Request"

//--------------------------------------------------------
// Rating
//--------------------------------------------------------

$(".like-button").on("click", function() {
  let likeButton = $(this);
  let articleId = likeButton.data("article-id");
  let likeCountElement = likeButton.find(".like-count"); 

  $.ajax({
    url: "/api/v1/update_like_count",
    method: "POST",
    data: JSON.stringify({ articleId: articleId }),
    contentType: "application/json",
    success: function(response) {

      if (response === 0) {
        let currentCount = parseInt(likeCountElement.text());
        likeCountElement.text(currentCount + 1);
        likeButton.addClass("liked");

      } else if (response === 2) {
        let currentCount = parseInt(likeCountElement.text());
        likeCountElement.text(currentCount - 1);
        likeButton.removeClass("liked");
      }

      else if (response === 1){
        console.log("Your account was not found, register!")
      }
    },
    error: function(xhr, status, error) {
      console.log("Error updating like count:", error);
    }
  });
});

//--------------------------------------------------------
// Скрытые комментарии.
//--------------------------------------------------------

$(document).ready(function() {
  $(".show-more").click(function() {
      $(this).siblings(".hidden-comments").slideDown();
      $(this).hide();
  });
});

//--------------------------------------------------------
// Отмечаем активный комментарий.
//--------------------------------------------------------

$(".comment").click(function() {
// Удаляем класс .active у всех комментариев
$(".comment").removeClass("active");
// Устанавливаем класс .active для выбранного комментария
$(this).addClass("active");
});

//--------------------------------------------------------
// Отправка комментария.
//--------------------------------------------------------

$(document).ready(function() {
  $(".comment-submit").on('click', async function(e) {
    e.preventDefault();
  
    // Находим родительский элемент .comment, чтобы получить данные статьи
    let activeComment = $(this).closest('.comment');
    let articleId = activeComment.data('article-id');
  
    // Находим поле ввода комментария и получаем его значение
    let commentInput = activeComment.find('.comment-input');
    let commentContent = commentInput.val();
  
    // Отправляем запрос с комментарием и ID статьи
    let result = await createComment(articleId, commentContent);
  
    if (result === 0) {
      console.log("Comment submitted successfully");
      // Очистить поле ввода комментария
      commentInput.val('');
    } 
    else {console.error("Error submitting comment:", result);}
  });
});

async function createComment(articleId, commentContent) {
  try {
    const response = await fetch('/api/v1/add_comment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        articleId: articleId,
        content: commentContent
      })
    });
    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Error:", error);
  }
}