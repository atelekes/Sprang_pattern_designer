extends Camera2D


var dragging: bool = false

func _ready() -> void:
	make_current()
	position = Vector2(get_viewport_rect().size.x / 4, get_viewport_rect().size.y / 4)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			if get_viewport().gui_get_focus_owner() == null:
				_zoom_at_point(true, get_global_mouse_position())
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			if get_viewport().gui_get_focus_owner() == null:
				_zoom_at_point(false, get_global_mouse_position())
		elif event.button_index == MOUSE_BUTTON_MIDDLE:
			dragging = event.pressed
		
	if event is InputEventMouseMotion and dragging:
		position -= event.relative / zoom
		force_update_transform()
		get_node("../Grid").queue_redraw()
func _zoom_at_point(zoom_in: bool, pos: Vector2) ->void:
	if zoom_in:
		zoom *= 1.1
	else:
		zoom /= 1.1
	force_update_scroll()
	position += pos - get_global_mouse_position()
	force_update_transform()
	get_node("../Grid").queue_redraw()
	
