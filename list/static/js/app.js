$(document).ready(function(){
	dragDrop()

	$(window).on('scroll', function() {
		$('.list-item').removeClass('visible-options');
	})

	$('a.filter-link').on('click', function(e) {
		e.preventDefault()
		$link = $(this)
		if ($link.hasClass('active')) {
			$('li.deleted').addClass('display-none');
		} else if ($link.hasClass('all')) {
			$('li.deleted').removeClass('display-none');
		}
	})

	$('.edit-user ul').on('click', 'li a', function(e) {
		e.preventDefault()
		var hash = this.hash
		$('.selected').removeClass('selected')
		$(this.closest('li')).addClass('selected');
		$(hash).addClass('selected');
	})

	$('.kitchen-lists').on('click', 'li.list-item p', function(){
		var $item = $(this).closest('.list-item')
		var $dropdown = $item.find('.list-forms')
		var $itemBox = $item.closest('.kitchen-list')
		if ($item.hasClass('visible-options')){
			$('.visible-options').removeClass('visible-options')
			$itemBox.removeClass('high-z')
		} else {
			var t = $item.offset().top + $item.height() - 7
			var l = $item.offset().left + ($item.width()/2 - $dropdown.width()/2)
			var fh = $('.list-forms').height()
			// make sure dropdown is not cut off by bottom/side of page!
			if ($(window).height() - t < fh) {
				t -= ( fh + $item.height() )
				t += 10
			}
			$('.visible-options').removeClass('visible-options')
			$('.kitchen-list.high-z').removeClass('high-z')
			$item.toggleClass('visible-options')
			$dropdown.offset({top: t, left: l})
			$itemBox.addClass('high-z')
		}
	})

	$('.kitchen-lists').on('click', 'li .edit-form', function(){
		event.preventDefault()
			$('.high-z').removeClass('high-z')
			var $modalBox = $('.general-modal')
			var title = $('.kitchen-title').text()
		$.ajax({
			url: this.action,
			error: function(response){
				$modalBox.addClass('error-modal').on('click', '.modal-close-x', function(e){
					event.preventDefault()
					var modalClass = 'error-modal'
					var modalBox = $(this).closest('.general-modal')
					closeModal($modalBox, modalClass)
				})
				$modalBox.find('h5').text('Error loading details')
				$modalBox.find('.modal-main').html('<h5>Error Page</h5>')
			},
			success: function(response){
				$('.page-overlay').removeClass('display-none')
				$modalBox.addClass('item-detail-modal').on('click', '.modal-close-x', function(e){
					// event.preventDefault()
					var modalClass = 'item-detail-modal'
					var $modalBox = $(this).closest('.general-modal')
					closeModal($modalBox, modalClass)
				})
				$modalBox.find('h5').text(title)
				$modalBox.find('.modal-main').html(response)
				$modalBox.removeClass('display-none')
			}
		})
	})

	$('body').on('submit', '.update-note-form', function(){
		event.preventDefault()
		$.ajax({
			url: this.action,
			method: this.method,
			data: $(this).serialize(),
			success: function(response){
				$('.modal-main').html(response)
			},
			error: function(response){
				console.log('failed')
			} 
		})
	})

	function closeModal(modal, modalClass) {
		modal.addClass('display-none')
		modal.find('.modal-main').html('')
		modal.find('h5').text('')
		modal.removeClass(modalClass)
		$('.page-overlay').addClass('display-none')
	}

	$('.general-modal').on('click', '.edit-item-notes', function(){
		var showForm = $(this).closest('.general-modal').find('.update-note-form')
		var hideButton = $(this)
		formToggle(hideButton, showForm)
	})

	$('.add-item').on('click', function(){
		$modalBox = $('.general-modal')
		$itemForm = $('.add-item-form').clone()
		$('.page-overlay').removeClass('display-none')
		$modalBox.addClass('add-item-modal').on('click', '.modal-close-x', function(e){
			var modalClass = 'add-item-modal'
			var $modalBox = $(this).closest('.general-modal')
			closeModal($modalBox, modalClass)
		})
		$modalBox.find('h5').text('Add Item')
		$modalBox.find('.modal-main').append($itemForm)
		$itemForm.removeClass('display-none')
		$modalBox.removeClass('display-none')
	})

	$('.open-kitchen-form').on('click', function(){
		$modalBox = $('.general-modal')
		$kitchenForm = $('.new-kitchen-form').clone()
		$('.page-overlay').removeClass('display-none')
		$modalBox.addClass('.new-kitchen-modal').on('click', '.modal-close-x', function(e){
			var modalClass = 'new-kitchen-modal'
			var $modalBox = $(this).closest('.general-modal')
			closeModal($modalBox, modalClass)
		})
		$modalBox.find('h5').text('Create Kitchen')
		$modalBox.find('.modal-main').append($kitchenForm)
		$kitchenForm.removeClass('display-none')
		$modalBox.removeClass('display-none')
	})

	$('.general-modal').on('click', '.cancel-link', function(){
		if ( $(this).closest('form').hasClass('update-note-form') ) {
			var hideForm = $(this).closest('form')
			var showButton = $('.edit-item-notes')
			formToggle(hideForm, showButton)
		} else {
			$modal = $('.general-modal')
			$modal.attr('class', '.general-modal')
			$modal.addClass('display-none')
			$modal.find('.modal-main').html('')
			$modal.find('h5').text('')
			$('.page-overlay').addClass('display-none')
		}
	})

	$('.kitchen-lists').on('click', 'h6 a', function(){
		var firstList = $('.kitchen-list').first()[0]
		var clickedList = $(this).closest('.kitchen-list')[0]
		if ( firstList != clickedList ){
			var newFirstList = $($(clickedList).find('ul')[0])
			var newBottomList = $($(firstList).find('ul')[0])
			$(clickedList).html(newBottomList)
			$(firstList).html(newFirstList)
			dragDrop()		
		}
	})

	$('body').on('click', function(e){
		$target = $(e.target)
		if (!$target.parent().hasClass('list-item')){
			$('.visible-options').removeClass('visible-options')
			$('.kitchen-list.high-z').removeClass('high-z')
		}
	})

	function formToggle(hide, show) {
		$(hide).addClass('display-none')
		$(show).removeClass('display-none')
	}

	function dragDrop() {
		$('.list-item').draggable({
			revert: 'invalid',
			revertDuration: 700,
			scroll: false,
			distance: 5,
			appendTo: 'body',
			helper: 'clone',
			start: function(){
				var $li = $(this)
				var $box = $('#drag-box')
				$('.kitchen-list.high-z').removeClass('high-z')
				$('.visible-options').removeClass('visible-options')
				$li.data("origPosition", $li.position())
				$('.kitchen-list').css('overflow', 'hidden')
				$li.css('opacity', '0.4')
			},
			drag: function(){
				// debugger;
				var $list = $(this).closest('.kitchen-list')
				$($list[0]).droppable({disabled: true})
			},
			stop: function(){
				$(this).css('opacity', '1')
			}
		});
		$('.kitchen-list').droppable({
			accept: '.list-item',
			drop: function(event, ui){
				var droppedAt = $($(event.target).find('ul')[0])
				var wantedForm = $(droppedAt).attr('id').slice(2)
				var formToSubmit = $(ui.draggable[0]).find("form[class*="+ wantedForm +"]")
				$.ajax({
					url: formToSubmit.attr('action'),
					dataType: 'json',
					type: formToSubmit.attr('method'),
					data: {
						'csrfmiddlewaretoken': $(formToSubmit[0]).find("input[name='csrfmiddlewaretoken']").val(),
						'item-status': $(formToSubmit[0]).find("input[name='item-status']").val()
					},
					error: function(){
						console.log('fail');
						ui.draggable.animate(ui.draggable.data().origPosition, "slow")
					},
					success: function(response){
						$(ui.draggable[0]).remove()
						$(droppedAt).append(response)
						$('.kitchen-list').droppable("option", "disabled", false)
						$('.kitchen-list').css('overflow-y', 'auto')
						dragDrop()
					}
				})
			}
		})
		$('.list-item').children().draggable({ disabled: true });
	}
})
