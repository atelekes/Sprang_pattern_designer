extends Node2D

signal full_draw_complete

var prev_row: int = Global.row
var prev_column: int = Global.column

const Markscene := preload("res://scenes/Marks.tscn")
const Helperscene := preload("res://scenes/helper.tscn")

var marks := {}
var selected_type := ""

var box_selection := false
var box_start : Vector2 = Vector2.ZERO
var selected_marks := {}
var box_rect: Rect2 = Rect2()

var clipboard := []

var moving_group := []   # array of {mark: Node2D, offset: Vector2i}
var draw_all:bool = false

var stop_delete := false

var pasted := false

var line_count := {}
var orange_count := []
var white_count := []

var bg_color := Color8(77, 77, 77)

func _set_tool(type: String) -> void: #load a mark to preview (hover it)
	selected_type = type
	if Global.preview_mark == null:
		Global.preview_mark = Markscene.instantiate()
		Global.preview_mark.mark_type = type
		add_child(Global.preview_mark)
	else:
		Global.preview_mark.mark_type = type
		Global.preview_mark._update_width()
	Global.preview_mark.position = Vector2i(Global.column  * Global.cell_width, Global.row * Global.cell_height)
	Global.preview_mark.queue_redraw()

func _ready() -> void: #indicators's path
	Global.RowIndicator = $"../CanvasLayer/Control/UI/CurrentRow"
	Global.ColumnIndicator = $"../CanvasLayer/Control/UI/CurrentColumn"
	Global.mark_changed.connect(_mark_changed)
	if Global.load_path != "":
		call_deferred("_load_from_png", Global.load_path)
		Global.load_path = ""
	Global.mark_changed.emit()
	
func _on_mark_deleted(mark: Node2D, skip: bool = true) -> void: #delete or select the hovered mark
	if Input.is_key_pressed(KEY_CTRL):
		if not mark.selected:
			mark.selected = true
			mark.queue_redraw()
			selected_marks[Vector2(int(mark.position.x/Global.cell_width), 
			int(mark.position.y/Global.cell_height))] = mark
		else:
			mark.selected = false
			mark.queue_redraw()
			selected_marks.erase(Vector2(int(mark.position.x/Global.cell_width), 
			int(mark.position.y/Global.cell_height)))
	else:
		if stop_delete:
			stop_delete = false
		else:
			if mark.selected and skip:
				_delete_selected()
			else:
				for key in marks.keys():
					if not is_instance_valid(marks[key]):
						marks.erase(key)
						continue
					if marks[key] == mark:
						marks.erase(key)
						queue_redraw()
						break
				mark.queue_free()
			Global.mark_changed.emit()

func _on_mark_picked_up(mark: Node2D) -> void: #pick up the hovered mark
	if mark.selected and selected_marks.size() > 1 and moving_group.is_empty():
		Global.group_moving_active = true
		_pick_up_selected()
	else:
		for key in marks.keys():
			if not is_instance_valid(marks[key]):
				marks.erase(key)
				continue
			if marks[key] == mark:
				marks.erase(key)
				break
		Global.preview_mark = mark
		selected_type = mark.mark_type
	Global.mark_changed.emit()

func _pick_up_selected() -> void: #pick up all selected marks
	moving_group.clear()
	
	var min_col := 999999
	var min_row := 999999
	for key in selected_marks.keys():
		if not is_instance_valid(selected_marks[key]):
			selected_marks.erase(key)
			continue
		min_col = min(min_col, int(key.x))
		min_row = min(min_row, int(key.y))
	var offset_col = Global.column - min_col
	var offset_row = Global.row - min_row
	
	for key in selected_marks.keys():
		if not is_instance_valid(selected_marks[key]):
			selected_marks.erase(key)
			continue
		var mark = selected_marks[key]
		moving_group.append({
			"mark": mark,
			"offset": Vector2i(int(key.x) - min_col - offset_col , int(key.y) - min_row - offset_row)
		})
		marks.erase(key)
	Global.mark_changed.emit()

func _update_selection() -> void: # box selection
	if not Input.is_key_pressed(KEY_CTRL):
		for key in selected_marks.keys():
			if not is_instance_valid(selected_marks[key]):
				selected_marks.erase(key)
				continue
			selected_marks[key].selected = false
			selected_marks[key].queue_redraw()
		selected_marks.clear()
	
	
	for key in marks.keys():
		if not is_instance_valid(marks[key]):
			marks.erase(key)
			continue
		var mark = marks[key]
		var shape: RectangleShape2D = mark.get_node("Area2D/CollisionShape2D").shape
		var mark_rect := Rect2(mark.position, shape.size)
		if box_rect.intersects(mark_rect):
			mark.selected = true
			mark.queue_redraw()
			selected_marks[key] = mark
	box_rect = Rect2()

func _delete_selected() -> void: #delete all selected marks
	for key in selected_marks.keys():
		if not is_instance_valid(selected_marks[key]):
			selected_marks.erase(key)
			continue
		_on_mark_deleted(selected_marks[key], false)
	selected_marks.clear()
	Global.mark_changed.emit()

func _copy_selected() -> void: #copy all selected marks to clipboard (array)
	clipboard.clear()
	if selected_marks.is_empty():
		return
	
	var min_col = 99999
	var min_row = 99999
	for key in selected_marks.keys():
		if not is_instance_valid(selected_marks[key]):
			selected_marks.erase(key)
			continue
		min_col = min(min_col, int(key.x))
		min_row = min(min_row, int(key.y))
	for key in selected_marks.keys():
		var mark = selected_marks[key]
		clipboard.append({
			"type": mark.mark_type,
			"offset": Vector2i(int(key.x) - min_col, int(key.y) - min_row)
		})

func _paste_clipboard() -> void: #paste copied marks from clipboard
	moving_group.clear()
	if clipboard.is_empty() or not Global.inside:
		return
	var min_col = 99999
	var min_row = 99999
	for entry in clipboard:
		var new_col = Global.column + entry["offset"].x
		var new_row = Global.row + entry["offset"].y
		min_col = min(min_col, new_col)
		min_row = min(min_row, new_row)
		
	for entry in clipboard:
		var new_col = Global.column + entry["offset"].x
		var new_row = Global.row + entry["offset"].y
		
		if new_col < 0 or new_col >= Global.columns or new_row < 0 or new_row >= Global.rows:
			continue
		if marks.has(Vector2(new_col, new_row)):
			continue
		
		var new_mark = Markscene.instantiate()
		new_mark.mark_type = entry["type"]
		add_child(new_mark)
		new_mark.position = Vector2i(new_col * Global.cell_width, new_row * Global.cell_height)
		new_mark.untouchable = true
		new_mark.mark_deleted.connect(_on_mark_deleted)
		new_mark.mark_picked_up.connect(_on_mark_picked_up)
		
		moving_group.append({
			"mark": new_mark,
			"offset": Vector2i(int(new_col) - min_col, int(new_row) - min_row)
		})
		pasted = true

func _mirror_moved(type: String) -> void:
	var max_col = 0
	var max_row = 0
	for entry in moving_group:
		max_col = max(max_col, entry["offset"][0])
		max_row = max(max_row, entry["offset"][1])
	if type == "v":
		for entry in moving_group:
			entry["offset"][0] = max_col - entry["offset"][0] - entry["mark"].width
			var m = entry["mark"]
			if m.mark_type == "blue":
				m.mark_type = "green"
				continue
			if m.mark_type == "green":
				m.mark_type = "blue"
	else:
		for entry in moving_group:
			entry["offset"][1] = max_row - entry["offset"][1]
	for entry in moving_group:
		var m = entry["mark"]
		var offset = entry["offset"]
		m.position = Vector2i((Global.column + offset.x) * Global.cell_width, 
		(Global.row + offset.y) * Global.cell_height)
		m.queue_redraw()
	Global.group_moving_active = false

func _hide_UI() -> void:
	Global.UI_visibility = not Global.UI_visibility
	get_node("../CanvasLayer/Control").visible = Global.UI_visibility

func _toggle_night_mode() -> void:
	Global.night_mode = not Global.night_mode
	var text_color: Color
	if Global.night_mode:
		text_color = Color8(246, 246, 246)
		bg_color = Color8(77, 77, 77)
		RenderingServer.set_default_clear_color(Color8(77, 77, 77))
	else:
		text_color = Color.BLACK
		bg_color = Color8(255, 255, 255)
		RenderingServer.set_default_clear_color(Color.WHITE)
	$"../CanvasLayer/Control/UI/RowsH/RowsSpinBox".add_theme_color_override("font_color", text_color)
	$"../CanvasLayer/Control/UI/RowsH/RowsSpinBox/RowsLabel".add_theme_color_override("font_color", text_color)
	$"../CanvasLayer/Control/UI/ColumnsH/ColumnsSpinBox".add_theme_color_override("font_color", text_color)
	$"../CanvasLayer/Control/UI/ColumnsH/ColumnsSpinBox/ColumnsLabel".add_theme_color_override("font_color", text_color)
	$"../CanvasLayer/Control/UI/CurrentRow".add_theme_color_override("font_color", text_color)
	$"../CanvasLayer/Control/UI/CurrentColumn".add_theme_color_override("font_color", text_color)
	$"../CanvasLayer/Control/UI/NightMode".add_theme_color_override("font_color", text_color)
	$"../CanvasLayer/Control/UI/RowTracker".add_theme_color_override("font_color", text_color)
	queue_redraw()

func _night_mode_button_toggled(toggled_on: bool) -> void: #UI button for night mode
	_toggle_night_mode()

func _get_visible_rect() -> Rect2: #returns the viewport's Rect
	var camera := get_viewport().get_camera_2d()
	var viewport_size := get_viewport_rect().size
	var half_size := (viewport_size / camera.zoom) / 2
	var top_left := camera.get_screen_center_position() - half_size
	return Rect2(top_left, half_size * 2)

func _on_image_save_button_down() -> void:
	if OS.has_feature("web"):
		_on_save_dialog_file_selected("1")
	else:
		$"../SaveDialog".popup_centered()

func _build_save_data() -> Dictionary:
	var marks_data := []
	for key in marks.keys():
		if not is_instance_valid(marks[key]):
			continue
		var mark = marks[key]
		marks_data.append({
			"col": int(key.x),
			"row": int(key.y),
			"type": mark.mark_type,
			"state": mark.state
		})
		
	return {
		"rows": Global.rows,
		"columns": Global.columns,
		"marks": marks_data
	}

func _on_save_dialog_file_selected(path: String) -> void:
	var capture_viewport:= $"../CaptureViewport"
	var full_width := Global.columns * Global.cell_width
	var full_height := Global.rows * Global.cell_height
	capture_viewport.size = Vector2i(full_width, full_height)
	capture_viewport.transparent_bg = false
	capture_viewport.render_target_update_mode = SubViewport.UPDATE_ONCE
	var was_night_mode :bool = false
	if Global.night_mode:
		was_night_mode = true
		$"../CanvasLayer/Control/UI/NightMode".button_pressed = not Global.night_mode
	
	var original_parent := get_parent()
	var original_position := position
	
	await get_tree().process_frame
	original_parent.remove_child(self)
	capture_viewport.add_child(self)
	position = Vector2.ZERO
	
	draw_all = true
	queue_redraw()
	await full_draw_complete
	await RenderingServer.frame_post_draw
	
	var img = capture_viewport.get_texture().get_image()
	
	var save_data := _build_save_data()
	var json_string := JSON.stringify(save_data)
	
	if OS.has_feature("web"):
		var png_buffer: PackedByteArray = img.save_png_to_buffer()
		var embed_bytes: PackedByteArray = ("\nSPRANG_DATA:" + json_string).to_utf8_buffer()
		png_buffer.append_array(embed_bytes)
		
		var file_name: String = path.get_file()
		if file_name.is_empty():
			file_name = "project.png"
		if not file_name.ends_with(".png"):
			file_name += ".png"
			
		var json_file_name: String = file_name.get_basename() + ".json"
		
		JavaScriptBridge.download_buffer(png_buffer, file_name, "image/png")
		JavaScriptBridge.download_buffer(json_string.to_utf8_buffer(), json_file_name, "application/json")
	else:
		img.save_png(path)
		var file := FileAccess.open(path, FileAccess.READ_WRITE)
		file.seek_end()
		file.store_string("\nSPRANG_DATA:" + json_string)
		file.close()
		
		var json_path := path.get_basename() + ".json"
		var json_file := FileAccess.open(json_path, FileAccess.WRITE)
		json_file.store_string(json_string)
		json_file.close()
	
	capture_viewport.remove_child(self)
	original_parent.add_child(self)
	position = original_position
	if was_night_mode:
		$"../CanvasLayer/Control/UI/NightMode".button_pressed = not Global.night_mode
	queue_redraw()

func _find_bytes(haystack: PackedByteArray, needle: PackedByteArray) -> int:
	var haystack_len := haystack.size()
	var needle_len := needle.size()
	for i in range(haystack_len - needle_len, -1, -1):
		var match_found := true
		for j in range(needle_len):
			if haystack[i + j] != needle[j]:
				match_found = false
				break
		if match_found:
			return i
	return -1

func _load_from_png(path: String) -> void:
	var data: Dictionary
	if path.get_extension().to_lower() == "json":
		var file := FileAccess.open(path, FileAccess.READ)
		var json_string := file.get_as_text()
		file.close()
		
		var json := JSON.new()
		if json.parse(json_string) != OK:
			return
		data = json.data
	else:
		var file := FileAccess.open(path, FileAccess.READ)
		var bytes := file.get_buffer(file.get_length())
		file.close()

		var marker := "SPRANG_DATA:".to_utf8_buffer()
		var idx = _find_bytes(bytes, marker)
		if idx == -1:
			return
		
		var json_bytes := bytes.slice(idx + marker.size())
		var json_string := json_bytes.get_string_from_utf8()
		
		var json := JSON.new()
		if json.parse(json_string) != OK:
			return
		data = json.data
	
	Global.rows = data["rows"]
	$"../CanvasLayer/Control/UI/RowsH/RowsSpinBox".value = data["rows"]
	Global.columns = data["columns"]
	$"../CanvasLayer/Control/UI/ColumnsH/ColumnsSpinBox".value = data["columns"]
	
	for key in marks.keys():
		if is_instance_valid(marks[key]):
			marks[key].queue_free()
	marks.clear()
	
	for entry in data["marks"]:
		var new_mark = Markscene.instantiate()
		new_mark.mark_type = entry["type"]
		new_mark.state = entry["state"]
		add_child(new_mark)
		new_mark.position = Vector2i(int(entry["col"]) * Global.cell_width, int(entry["row"]) * Global.cell_height)
		new_mark.untouchable = true
		new_mark.mark_deleted.connect(_on_mark_deleted)
		new_mark.mark_picked_up.connect(_on_mark_picked_up)
		marks[Vector2(entry["col"], entry["row"])] = new_mark
	
	queue_redraw()
	Global.mark_changed.emit()
	
func _on_row_tracker_toggled(toggled_on: bool) -> void:
	get_viewport().gui_release_focus()
	Global.row_tracker = not Global.row_tracker
	weave_mode_redraw()

func weave_mode_redraw() -> void:
	queue_redraw()
	for m in marks:
		marks[m].queue_redraw()

func _on_helper_button_down() -> void:
	var tree = get_tree()
	Global.saved_scene = get_tree().current_scene
	Global.saved_scene.process_mode = Node.PROCESS_MODE_DISABLED
	await get_tree().process_frame
	tree.root.remove_child(get_tree().current_scene)
	var helper := Helperscene.instantiate()
	tree.root.add_child(helper)
	tree.current_scene = helper

func _mark_changed() -> void:
	line_count.clear()
	for m in orange_count:
		m.num = ""
		m.queue_redraw()
	orange_count.clear()
	for w in white_count:
		w.num = ""
		w.queue_redraw()
	white_count.clear()
	for r in range(Global.rows):
		var start: int = 0
		var end: int = Global.columns
		var ostart: int = 0
		var oend := 0
		var wstart := 0
		var wend := 0
		for c in range(Global.columns):
			if marks.has(Vector2(c, r)):
				end = c
				if (end - start) / 2 > 3:
					line_count[Vector2(start + 1 + r%2, r)] = int((end-start)/2)
				start = c + marks[Vector2(c, r)].width
				if marks[Vector2(c, r)].mark_type == "orange" and c > oend:
					ostart = c
					var ocount := 1
					var is_next_orange := true
					while is_next_orange:
						if marks.has(Vector2(c+ocount*4, r)):
							if marks[Vector2(c+ocount*4, r)].mark_type == "orange":
								ocount += 1
							else:
								is_next_orange = false
								oend = c+ocount*4
						else:
							is_next_orange = false
							oend = c+ocount*4
					if ocount > 3:
						var mark = marks[Vector2(ostart + int(ocount/2*4), r)]
						mark.num = str(ocount)
						mark.queue_redraw()
						orange_count.append(mark)
		
				elif marks[Vector2(c, r)].mark_type == "white" and c > wend:
					wstart = c
					var wcount := 1
					var is_next_white := true
					while is_next_white:
						if marks.has(Vector2(c+wcount*2, r)):
							if marks[Vector2(c+wcount*2, r)].mark_type == "white":
								wcount += 1
							else:
								is_next_white = false
								wend = c+wcount*2
						else:
							is_next_white = false
							wend = c+wcount*2
					if wcount > 3:
						var mark = marks[Vector2(wstart + int(wcount/2*2), r)]
						mark.num = str(wcount)
						mark.queue_redraw()
						white_count.append(mark)
		if start == 0:
			line_count[Vector2(start + 1 + r%2, r)] = int(Global.columns/2)
		else:
			if (Global.columns - start) / 2 > 3:
				line_count[Vector2(start + 1 + r%2, r)] = int((Global.columns-start)/2)
		if start == 0:
			line_count[Vector2(start + 1 + r%2, r)] = int(Global.columns/2)
		else:
			if (Global.columns - start) / 2 > 3:
				line_count[Vector2(start + 1 + r%2, r)] = int((Global.columns-start)/2)
	queue_redraw()

func _draw() -> void:
	var col_start := 0
	var col_end := Global.columns
	var row_start := 0
	var row_end := Global.rows
	if not draw_all:
		var visible_rect := _get_visible_rect()
		col_start = max(0, int(visible_rect.position.x / Global.cell_width) - 1)
		col_end = min(Global.columns, int((visible_rect.position.x + visible_rect.size.x) / Global.cell_width) + 1)
		row_start = max(0, int(visible_rect.position.y / Global.cell_height) - 1)
		row_end = min(Global.rows, int((visible_rect.position.y + visible_rect.size.y) / Global.cell_height) + 1)
		for r in range(row_start, row_end+1):
			draw_line(Vector2(0, r * Global.cell_height), 
			Vector2(Global.columns * Global.cell_width, r * Global.cell_height), Color.BLACK, 3)
			
		for c in range(col_start, col_end+1):
			draw_line(Vector2(c * Global.cell_width, 0), 
			Vector2(c * Global.cell_width, Global.rows * Global.cell_height), Color.BLACK, 3)
			
		if get_node("../Camera2D").zoom > Vector2(0.3, 0.3):
			for r in range(row_start, row_end):
				for c in range(col_start, col_end):
					if line_count.has(Vector2(c, r)):
						draw_rect(Rect2((c+1)*Global.cell_width-1.5, r*Global.cell_height+1.5,
						3, Global.cell_height-3), bg_color)
						
						draw_string(ThemeDB.fallback_font,
						Vector2((c+0.5)*Global.cell_width+1, (r+0.7)*Global.cell_height), 
						str(line_count[Vector2(c, r)]),
						HORIZONTAL_ALIGNMENT_CENTER, -1, 16, Color.BLACK)
					else:
						if (c + r % 2 ) % 2 == 0 and c != Global.columns-1:
							draw_line(Vector2(Global.cell_width*(c + 0.5), Global.cell_height*(r+0.5)), 
							Vector2(Global.cell_width*(c+1.5), Global.cell_height*(r+0.5)), Color.BLACK, 3)
		if Global.inside:
			draw_rect(Rect2(Global.column * Global.cell_width, Global.row * Global.cell_height,
			Global.cell_width, Global.cell_height), Color.GRAY, false, 3.0)
	else:
		for r in range(Global.rows+1):
			draw_line(Vector2(0, r * Global.cell_height), 
			Vector2(Global.columns * Global.cell_width, r * Global.cell_height), Color.BLACK, 3)
			
		for c in range(Global.columns+1):
			draw_line(Vector2(c * Global.cell_width, 0), 
			Vector2(c * Global.cell_width, Global.rows * Global.cell_height), Color.BLACK, 3)
			
		for r in range(Global.rows):
			for c in range(Global.columns):
				if line_count.has(Vector2(c - r%2, r)):
					draw_rect(Rect2((c+1)*Global.cell_width-1.5, r*Global.cell_height+1.5,
					3, Global.cell_height-3), bg_color)
						
					draw_string(ThemeDB.fallback_font, 
					Vector2((c+0.5)*Global.cell_width+1, (r+0.7)*Global.cell_height), 
					str(line_count[Vector2(c - r%2, r)]),
					HORIZONTAL_ALIGNMENT_CENTER, -1, 16, Color.BLACK)
				else:
					if (c + r % 2 ) % 2 == 0 and c != Global.columns-1:
						draw_line(Vector2(Global.cell_width*(c + 0.5), Global.cell_height*(r+0.5)), 
						Vector2(Global.cell_width*(c+1.5), Global.cell_height*(r+0.5)), Color.BLACK, 3)
		draw_all = false
		full_draw_complete.emit()
		
	for key in marks.keys():
		if key.y < row_start or key.y > row_end or key.x < col_start or key.x > col_end:
			continue
		var mark = marks[key]
		if mark.mark_type == "blue" or mark.mark_type == "green" or mark.mark_type == "orange":
			var next_key = Vector2(key.x+mark.width, key.y)
			if marks.has(next_key):
				var hole_color: Color
				if Global.night_mode:
					hole_color = Color.WHITE
				else:
					hole_color = Color.BLACK
				var next_mark = marks[next_key]
				if next_mark.mark_type == "blue" or next_mark.mark_type == "green" or next_mark.mark_type == "orange":
					draw_line(Vector2((key.x+mark.width)*Global.cell_width, (key.y-1)*Global.cell_height), 
					Vector2((key.x+mark.width)*Global.cell_width, (key.y+2)*Global.cell_height), hole_color, 8)
		
	if box_selection and not Global.row_tracker:
		draw_rect(box_rect, Color8(144, 213, 255, 50))
	
	if Global.row_tracker:
		draw_rect(Rect2(0, 0, Global.cell_width * Global.columns, Global.cell_height * Global.row_tracker_row), Color8(0, 0, 0, 150))
		
		draw_rect(Rect2(0, Global.cell_height * (Global.row_tracker_row + 1), Global.cell_width * Global.columns, 
		Global.cell_height * (Global.rows - Global.row_tracker_row - 1)), Color8(0, 0, 0, 150))

func _unhandled_input(event: InputEvent) -> void:
	stop_delete = false
	var pos := get_global_mouse_position()
	prev_row = Global.row
	prev_column= Global.column
	Global.row = int(pos.y / Global.cell_height)
	Global.column = int(pos.x / Global.cell_width)
	Global.inside = 0 <= Global.row  and Global.row < Global.rows and 0 <= Global.column and Global.column < Global.columns
	
	if Global.inside and (prev_row != Global.row or prev_column != Global.column):
		queue_redraw()
		Global.RowIndicator.text = "Row: %d" % [Global.row+1]
		Global.ColumnIndicator.text = "Column: %d" % [Global.column+1]
		
		if Global.preview_mark != null: #snapping the previewed mark to the cursor
			var shift_amount := 0
			for key in marks.keys():
				var mark = marks[key]
				if key.y != Global.row:
					continue
				var mark_start = key.x
				var mark_end = key.x + mark.width - 1
				var preview_start = Global.column
				var preview_end = Global.column + Global.preview_mark.width - 1
				if preview_start <= mark_end and preview_end >= mark_start:
					var pre_width = Global.preview_mark.width
					shift_amount = max(shift_amount, mark_end - preview_start + 1)
					#mark.untouchable = true
					if shift_amount >= mark.width:
						shift_amount = -(pre_width - (shift_amount-mark.width))
			Global.preview_mark.position = Vector2i((Global.column + shift_amount)  * Global.cell_width, 
			Global.row * Global.cell_height)
		
		if not moving_group.is_empty(): #snapping the selected moving marks to the cursor
			for entry in moving_group:
				var m = entry["mark"]
				var offset = entry["offset"]
				m.position = Vector2i((Global.column + offset.x) * Global.cell_width, 
				(Global.row + offset.y) * Global.cell_height)
				m.queue_redraw()
			Global.group_moving_active = false
		
		if box_selection:
			var end_pos = Vector2(Global.column * Global.cell_width, Global.row * Global.cell_height)
			var top_left = Vector2(min(box_start.x, end_pos.x), min(box_start.y, end_pos.y))
			var bottom_right = Vector2(max(box_start.x, end_pos.x) + Global.cell_width, max(box_start.y, end_pos.y) + Global.cell_height)
			box_rect = Rect2(top_left, bottom_right - top_left)
			queue_redraw()
		
	if event is InputEventMouseButton: #remove focus from the spinboxes
		if event.pressed and get_viewport().gui_get_focus_owner() != null:
			get_viewport().gui_release_focus()
		
		if event.button_index == MOUSE_BUTTON_LEFT and Global.preview_mark != null and Global.inside: #place preview
			var collide := false
			var pre_pos = Vector2(Global.preview_mark.position / Vector2(Global.cell_width, Global.cell_height))
			for n in Global.preview_mark.width:
				if marks.has(pre_pos + Vector2(n, 0)):
					collide = true
					break
			if not collide:
				marks[pre_pos] = Global.preview_mark
				marks[pre_pos].untouchable = true
				if not Global.preview_mark.mark_deleted.is_connected(_on_mark_deleted):
					Global.preview_mark.mark_deleted.connect(_on_mark_deleted)
					Global.preview_mark.mark_picked_up.connect(_on_mark_picked_up)
				Global.preview_mark = null
				stop_delete = true
			Global.mark_changed.emit()
		
		if event.button_index == MOUSE_BUTTON_LEFT and not moving_group.is_empty() and Global.inside:
			if not pasted:
				selected_marks.clear()
			for entry in moving_group: #placing the selected picked up marks
				var m = entry["mark"]
				var offset = entry["offset"]
				var new_col = Global.column + offset.x
				var new_row = Global.row + offset.y
				marks[Vector2(new_col, new_row)] = m
				m.position = Vector2i(new_col * Global.cell_width, new_row * Global.cell_height)
				m.untouchable = true
				if not pasted:
					selected_marks[Vector2(new_col, new_row)] = m
			pasted = false
				
			moving_group.clear()
			Global.mark_changed.emit()
			
		elif event.button_index == MOUSE_BUTTON_LEFT and event.pressed: #start box selection
			box_selection = true
			box_start = Vector2(Global.column * Global.cell_width, Global.row * Global.cell_height)
		elif event.button_index == MOUSE_BUTTON_LEFT and not event.pressed and box_selection:
			box_selection = false #end box selection
			_update_selection()
			
	
	if event is InputEventKey and event.pressed:
		var keycode = event.keycode
		if keycode == KEY_F1:
			call_deferred("_on_helper_button_down")

				
		elif keycode == KEY_H: #hide UI
			_hide_UI()
		elif keycode == KEY_N: #night mode
			$"../CanvasLayer/Control/UI/NightMode".button_pressed = not Global.night_mode
			
		if not Global.row_tracker:
			if keycode == KEY_1:
				_set_tool("blue")
			elif keycode == KEY_2:
				_set_tool("green")
			elif keycode == KEY_3:
				_set_tool("orange")
			elif keycode == KEY_4:
				_set_tool("pink")
			elif keycode == KEY_5:
				_set_tool("red")
			elif keycode == KEY_6:
				_set_tool("purple")
			elif keycode == KEY_7:
				_set_tool("white")
			elif keycode == KEY_ESCAPE: #deselect all
				if not moving_group.is_empty():
					for m in moving_group:
						m["mark"].queue_free()
					moving_group.clear()
				elif Global.preview_mark != null:
					Global.preview_mark.queue_free()
					Global.preview_mark = null
				else:
					for key in selected_marks.keys():
						if not is_instance_valid(selected_marks[key]):
							selected_marks.erase(key)
							continue
						selected_marks[key].selected = false
						selected_marks[key].queue_redraw()
					selected_marks.clear()
					box_rect = Rect2()
			elif keycode == KEY_C and event.ctrl_pressed: #copy
				_copy_selected()
			elif keycode == KEY_V and event.ctrl_pressed: #paste
				_paste_clipboard()
			elif keycode == KEY_DELETE or keycode == KEY_BACKSPACE: #delete all selected
				_delete_selected()
			elif keycode == KEY_S and event.ctrl_pressed:
				$"../SaveDialog".popup_centered()
			elif not moving_group.is_empty() and (keycode == KEY_LEFT or keycode == KEY_RIGHT):
				_mirror_moved("v")
			elif not moving_group.is_empty() and (keycode == KEY_UP or keycode == KEY_DOWN):
				_mirror_moved("h")
		
		else:
			if keycode == KEY_UP:
				if Global.row_tracker_row > 0:
					Global.row_tracker_row -= 1
					weave_mode_redraw()
			
			elif keycode == KEY_DOWN:
				if Global.row_tracker_row < Global.columns - 1:
					Global.row_tracker_row += 1
					weave_mode_redraw()
