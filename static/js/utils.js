$(document).ready(function () {

	function Reload() {
		{
			setTimeout(function () {
				location.reload(true);
			}, 500);

		}
	}


	function getCrsfCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			var cookies = document.cookie.split(';')
			for (var index = 0; index < cookies.length; index++) {
				var cookie = jQuery.trim(cookies[index]);
				if (cookie.substring(0, name.length + 1) === (name + "=")) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}

	var csrftoken = getCrsfCookie('csrftoken');

	$('#add-new-post').on('click', function () {
		article_id = $(this).attr('article-id');
		comment = $('textarea').val();
		if (comment.length) {
			data = {
				comment: comment,
				article_id: article_id,
				csrfmiddlewaretoken: csrftoken
			}
			$.ajax({
				type: "POST",
				url: create_comment_url,
				data: data,
				success: function (data) {
					counter = parseInt($('#comments-count').html());
					$('#comments-count').html(counter + 1);
					$('textarea').val('');
					$('.comments').prepend(data);
					$('#show-message').trigger('click');
				}
			});
		}
	});

	$('.hot-new-item').hover(function () {
		image_to_set = $(this).attr('image_path');
		$('#hot-image').attr('src', image_to_set);
	});

	$('.category-selector').on('click', function () {
		old_str = $(this).attr('href');
		new_str = old_str.slice(1, old_str.length);
		data = {
			category: new_str
		}
		$.ajax({
			type: "GET",
			url: display_articles_by_category_url,
			data: data,
			success: function (data) {
				$('#' + new_str).html('');
				$('#' + new_str).append(data);
			}
		})
	});

	$('.add-to-fav').on('click', function (e) {
		e.preventDefault();
		article_id = $(this).attr('article-id');
		data = {
			'article_id': article_id
		}
		$.ajax({
			type: "GET",
			url: add_article_to_favourites_url,
			data: data,
			success: function (data) {

			}
		});
	});
	/*-------------------------------------------------------*/
	$('.one-star').on('click', function (e) {
		e.preventDefault();
		query = 'one-star';
		article_id = $(this).attr('data-id');
		data_to_send = {
			query: query,
			article_id: article_id
		}
		$.ajax({
			type: "GET",
			url: user_reaction_url,
			data: data_to_send,
			success: function (data) {
				$('#star-count-' + article_id).html(data.total_stars);
				Reload();
			}
		})
	});

	$('.two-star').on('click', function (e) {
		e.preventDefault();
		query = 'two-star';
		article_id = $(this).attr('data-id');
		data_to_send = {
			query: query,
			article_id: article_id
		}
		$.ajax({
			type: "GET",
			url: user_reaction_url,
			data: data_to_send,
			success: function (data) {
				$('#star-count-' + article_id).html(data.total_stars);
				Reload();
			}
		})
	});

	$('.three-star').on('click', function (e) {
		e.preventDefault();
		query = 'three-star';
		article_id = $(this).attr('data-id');
		data_to_send = {
			query: query,
			article_id: article_id
		}
		$.ajax({
			type: "GET",
			url: user_reaction_url,
			data: data_to_send,
			success: function (data) {
				$('#star-count-' + article_id).html(data.total_stars);
				Reload();
			}
		})
	});

	$('.four-star').on('click', function (e) {
		e.preventDefault();
		query = 'four-star';
		article_id = $(this).attr('data-id');
		data_to_send = {
			query: query,
			article_id: article_id
		}
		$.ajax({
			type: "GET",
			url: user_reaction_url,
			data: data_to_send,
			success: function (data) {
				$('#star-count-' + article_id).html(data.total_stars);
				Reload();
			}
		})
	});

	$('.five-star').on('click', function (e) {
		e.preventDefault();
		query = 'five-star';
		article_id = $(this).attr('data-id');
		data_to_send = {
			query: query,
			article_id: article_id
		}
		$.ajax({
			type: "GET",
			url: user_reaction_url,
			data: data_to_send,
			success: function (data) {
				$('#star-count-' + article_id).html(data.total_stars);
				Reload();
			}
		})
	});
	/*-------------------------------------------------------------*/
	/*
		$(".rating a").on('click', function (e) {
			let value = $(this).data('value');
			article_id = $(this).attr('data-id');
			data_to_send = {
				score: value,
				article_id: article_id
			}
			$.ajax({
				type: "GET",
				url: user_reaction_url,
				data: data_to_send,
				success: function (data) {
					$('#votes-count-' + article_id).html(data.total_votes);
				}
			})
		});
	*/
});