<script lang="ts">
	let hidden = $state(false);
	let expand = $state(false);
	let height = $state("");

	function toExpand() {
		hidden = expand = true;
		height = "250px";
	}

	function close(event: MouseEvent) {
		const noteBar = document.getElementById("noteBar");
		if (!noteBar?.contains((event.target as Node) || null)) {
			hidden = expand = false;
			height = "54px";
		}
	}
</script>

<svelte:document onclick={close} />

<div class={["note-bar", expand && "expand"]} style:height id="noteBar">
	<input
		type="text"
		class="note-input"
		placeholder={expand ? "Title" : "Take a note...."}
		onclick={toExpand}
		id="noteInput"
	/>
	<button type="button" class={["todo-btn mt-2 me-2", hidden && "hidden"]} id="addTodoList">
	</button>
	<textarea class="note-textarea" placeholder="Take a note..." id="noteTextarea"></textarea>
</div>

<style>
	/* Note bar */

	.note-bar {
		position: relative;
		width: 600px;
		background-color: #11111b;
		border-radius: 8px;
		border: 1px solid #313244;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
		transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
		overflow: hidden;
		height: 54px;
		align-self: center;
	}

	.note-bar.expand {
		height: 400px;
		/* overflow-y: auto; */
		/* Un valor mayor que el máximo esperado */
	}

	.note-input {
		position: absolute;
		width: 600px;
		height: 54px;
		padding: 15px;
		border: none;
		border-radius: 8px;
		font-size: 16px;
		box-sizing: border-box;
		background-color: #11111b;
		color: #cdd6f4;
		outline: none;
	}

	.note-textarea {
		position: absolute;
		width: 600px;
		min-height: 200px;
		max-height: 400px;
		padding: 15px;
		border: none;
		border-radius: 8px;
		font-family: inherit;
		font-size: inherit;
		color: #cdd6f4;
		box-sizing: border-box;
		resize: none;
		opacity: 0;
		transition: opacity 0.3s ease;
		margin-top: 54px;
		outline: none;
		background-color: transparent;
	}

	.note-bar.expand .note-textarea {
		opacity: 1;
	}

	.hidden {
		display: none;
	}

	.todo-btn {
		position: absolute;
		top: 0;
		right: 0;
		background-color: transparent;
		border: none;
		padding: 5px;
		margin: 10px;
		border-radius: 10px;
	}

	.todo-btn:hover {
		background-color: #1e1e2e;
		cursor: pointer;
	}
</style>
