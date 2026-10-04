extends Control
const Markscene := preload("res://scenes/Marks.tscn")
const colors := ["blue", "green", "orange", "pink", "red", "purple", "white"]
const colors2 := ["white", "blue", "green", "orange", "pink", "red", "purple"]
var pre : Node2D
var pre2 : Node2D
var pre3 : Node2D

func _ready() -> void:
	for n in range(len(colors)):
		pre = Markscene.instantiate()
		pre.mark_type = colors[n]
		add_child(pre)
		if n < 3:
			pre.position = Vector2i(14, 570+40*n)
		else:
			pre.position = Vector2i(200, 570+40*(n-3))
		
	for n in range(len(colors2)):
		if n != 0:
			pre2 = Markscene.instantiate()
			pre2.mark_type = colors2[n]
			add_child(pre2)
			pre2.position = Vector2(600, 60+40*n)
		pre3 = Markscene.instantiate()
		pre3.state = "S"
		pre3.mark_type = colors2[n]
		add_child(pre3)
		pre3.position = Vector2(600, 400+40*n)
	queue_redraw()
		
func _draw() -> void:
	draw_rect(Rect2(601, 60, 38, 28), Color.WHITE)
	draw_line(Vector2(610, 75), Vector2(631, 75), Color.BLACK, 2)
	draw_line(Vector2(620, 60), Vector2(620, 88), Color.BLACK, 2)
	
func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed:
		if event.keycode == KEY_F1 or event.keycode == KEY_ESCAPE:
			_on_back_button_down()


func _on_back_button_down() -> void:
	get_tree().current_scene.queue_free()
	get_tree().root.add_child(Global.saved_scene)
	get_tree().current_scene = Global.saved_scene
	Global.saved_scene.process_mode = Node.PROCESS_MODE_INHERIT
