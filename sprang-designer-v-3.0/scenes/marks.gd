extends Node2D

signal mark_deleted(mark: Node2D)
signal mark_picked_up(mark: Node2D)

var mark_type:= ""
var hovered := false
var untouchable := false
var selected : bool = false
var state := "line"
var font: Font = load("res://scenes/ARIAL.TTF")
var pos: Vector2 = Vector2.ZERO
var width: int = 0
var num : String = ""


func _update_width() -> void:
	match mark_type:
		"blue", "green": width = 3
		"orange": width = 4
		"pink", "red", "purple", "white": width = 2

func _ready() -> void:
	_update_width()
	var shape := RectangleShape2D.new()
	shape.size = Vector2(Global.cell_width * width, Global.cell_height)
	$Area2D/CollisionShape2D.shape = shape
	$Area2D/CollisionShape2D.position = shape.size / 2
	
	$Area2D.mouse_entered.connect(_on_mouse_entered)
	$Area2D.mouse_exited.connect(_on_mouse_exited)
	$Area2D.input_event.connect(_on_input_event)
	Global.mark_changed.connect(_changed)
	
	var text_size := font.get_string_size("S", HORIZONTAL_ALIGNMENT_CENTER, -1, 20)
	pos = Vector2((Global.cell_width*width)/2 - text_size.x/2,
	Global.cell_height/2+text_size.y/4)
	
func _on_mouse_entered() -> void:
	hovered = true
	queue_redraw()

func _on_mouse_exited() ->void:
	hovered = false
	queue_redraw()	

func _changed() -> void:
	pass

func _on_input_event(viewport, event, shape_idx) -> void:
	if event is InputEventMouseButton and event.pressed and Global.preview_mark == null and not Global.group_moving_active and not Global.row_tracker:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if not untouchable:
				mark_deleted.emit(self)
		elif event.button_index == MOUSE_BUTTON_RIGHT:
			mark_picked_up.emit(self)
	
func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and (hovered or selected) and not Global.row_tracker:
		if event.keycode == KEY_Q:
			if state == "line":
				state = "S"
			else:
				state = "line"
			queue_redraw()

func _draw() -> void:
	untouchable = false
	if mark_type == "blue":
		if Global.row_tracker and not self.position[1] / Global.cell_height == Global.row_tracker_row:
			draw_rect(Rect2(1, 1, Global.cell_width*3-2,  Global.cell_height-2), Color8(0, 47, 88))
		elif hovered or selected:
			draw_rect(Rect2(1, 1, Global.cell_width*3-4,  Global.cell_height-4), Color8(143, 227, 255))
			draw_rect(Rect2(2, 2, Global.cell_width*3-5, Global.cell_width+5), Color.WHITE, false, 3)
		else:
			draw_rect(Rect2(1, 1, Global.cell_width*3-2,  Global.cell_height-2), Color8(113, 197, 238))
	
	elif mark_type == "green":
		if Global.row_tracker and not self.position[1] / Global.cell_height == Global.row_tracker_row:
			draw_rect(Rect2(1, 1, Global.cell_width*3-2,  Global.cell_height-2), Color8(14, 55, 0))
		elif hovered or selected:
			draw_rect(Rect2(1, 1, Global.cell_width*3-4,  Global.cell_height-4), Color8(194, 235, 87))
			draw_rect(Rect2(2, 2, Global.cell_width*3-5, Global.cell_width+5), Color.WHITE, false, 3)
		else:
			draw_rect(Rect2(1, 1, Global.cell_width*3-2,  Global.cell_height-2), Color8(164, 205, 57))
	
	elif mark_type == "orange":
		if Global.row_tracker and not self.position[1] / Global.cell_height == Global.row_tracker_row:
			draw_rect(Rect2(1, 1, Global.cell_width*4-2,  Global.cell_height-2), Color8(100, 3, 0))
		elif hovered or selected:
			draw_rect(Rect2(1, 1, Global.cell_width*4-4,  Global.cell_height-4), Color8(255, 183, 42))
			draw_rect(Rect2(2, 2, Global.cell_width*4-5, Global.cell_width+5), Color.WHITE, false, 3)
		else:
			draw_rect(Rect2(1, 1, Global.cell_width*4-2,  Global.cell_height-2), Color8(250, 153, 12))
	
	elif mark_type == "pink":
		if Global.row_tracker and not self.position[1] / Global.cell_height == Global.row_tracker_row:
			draw_rect(Rect2(1, 1, Global.cell_width*2-2,  Global.cell_height-2), Color8(67, 0, 16))
		elif hovered or selected:
			draw_rect(Rect2(1, 1, Global.cell_width*2-4,  Global.cell_height-4), Color8(247, 134, 196))
			draw_rect(Rect2(2, 2, Global.cell_width*2-5, Global.cell_width+5), Color.WHITE, false, 3)
		else:
			draw_rect(Rect2(1, 1, Global.cell_width*2-2,  Global.cell_height-2), Color8(217, 104, 166))
	
	elif mark_type == "red":
		if Global.row_tracker and not self.position[1] / Global.cell_height == Global.row_tracker_row:
			draw_rect(Rect2(1, 1, Global.cell_width*2-2,  Global.cell_height-2), Color8(12, 0, 0))
		elif hovered or selected:
			draw_rect(Rect2(1, 1, Global.cell_width*2-4,  Global.cell_height-4), Color8(192, 76, 63))
			draw_rect(Rect2(2, 2, Global.cell_width*2-5, Global.cell_width+5), Color.WHITE, false, 3)
		else:
			draw_rect(Rect2(1, 1, Global.cell_width*2-2,  Global.cell_height-2), Color8(162, 46, 33))
	
	elif mark_type == "purple":
		if Global.row_tracker and not self.position[1] / Global.cell_height == Global.row_tracker_row:
			draw_rect(Rect2(1, 1, Global.cell_width*2-2,  Global.cell_height-2), Color8(28, 4, 50))
		elif hovered or selected:
			draw_rect(Rect2(1, 1, Global.cell_width*2-4,  Global.cell_height-4), Color8(208, 184, 230))
			draw_rect(Rect2(2, 2, Global.cell_width*2-5, Global.cell_width+5), Color.WHITE, false, 3)
		else:
			draw_rect(Rect2(1, 1, Global.cell_width*2-2,  Global.cell_height-2), Color8(178, 154, 200))
	
	elif mark_type == "white":
		if Global.row_tracker and not self.position[1] / Global.cell_height == Global.row_tracker_row:
			draw_rect(Rect2(1, 1, Global.cell_width*2-2,  Global.cell_height-2), Color8(105, 105, 105))
		elif hovered or selected:
			draw_rect(Rect2(1, 1, Global.cell_width*2-4,  Global.cell_height-4), Color8(225, 225, 255))
			draw_rect(Rect2(2, 2, Global.cell_width*2-5, Global.cell_width+5), Color.WHITE, false, 3)
		else:
			draw_rect(Rect2(1, 1, Global.cell_width*2-2,  Global.cell_height-2), Color8(255, 255, 255))
	
	if not num == "":
		draw_string(ThemeDB.fallback_font, Vector2(Global.cell_width*(width*0.5 - 0.25), Global.cell_height*0.65),
		 num, HORIZONTAL_ALIGNMENT_CENTER, -0, 16, Color.BLACK)
	else:		
		if state == "line" and not mark_type == "white":
			draw_line(Vector2(Global.cell_width/2, Global.cell_height/2), 
			Vector2(Global.cell_width*(width-0.5), Global.cell_height/2), Color.BLACK, 2)
		else:
			draw_string(font, pos, "S", HORIZONTAL_ALIGNMENT_CENTER, -1, 20, Color.BLACK)
