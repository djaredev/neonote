<script lang="ts">
	import { fade } from "svelte/transition";
	import { Modal } from "$lib/components/Modal";
	import TextEditor from "$lib/components/Editor/TextEditor.svelte";
	import { getNoteState } from "$lib/state/note.svelte";

	let { class: className, children } = $props();

	const noteState = getNoteState();

	const note = $state({
		title: "",
		content: ""
	});

	function customCenter(width: number, height: number) {
		return {
			left: (window.innerWidth - width) / 2,
			top: (window.innerHeight - height) / 3
		};
	}

	let transition = {
		type: fade,
		duration: { duration: 100 }
	};

	function onClose() {
		noteState.create($state.snapshot(note));
		console.log("Close modal..");
		console.log(noteState.notes.length);
		note.title = "";
		note.content = "";
	}

	let outside: HTMLElement;

	function onOpen() {
		document.body.appendChild(outside);
	}
</script>

<Modal.Root class="make-note" {onClose} {onOpen} {customCenter}>
	<Modal.Preview class={className}>
		{@render children()}
	</Modal.Preview>
	<div bind:this={outside}>
		<Modal.Overlay class="overlay-make-note" {transition} />
		<Modal.View class="make-note-view">
			<TextEditor class="note-title-expand" bind:value={note.title} placeholder="Title" />
			<TextEditor class="note-body-expand" bind:value={note.content} placeholder="Take a note..." />
		</Modal.View>
	</div>
</Modal.Root>

<style>
	:global(.make-note-view) {
		position: fixed;
		display: flex;
		flex-direction: column;
		width: 600px;
		max-height: 824px;
		color: white;
		background: #11111b;
		border: 1px solid #313244;
		border-radius: 10px;
		overflow: hidden;
		transition: all 0.1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
		user-select: none;
		font-size: 1rem;
		box-sizing: border-box;
		z-index: 2000;
	}

	@media (width <= 600px) {
		:global(.make-note-view) {
			max-width: 100%;
			max-height: 412px;
		}
	}

	:global(.note-title-expand) {
		padding: 15px;
		min-height: 50px;
		max-height: 100px;
		font-weight: bold;
		background: inherit;
		outline: none;
		box-sizing: border-box;
		overflow: scroll;
	}

	:global(.note-body-expand) {
		min-height: 60px;
		flex-grow: 1;
		padding: 15px;
		background: inherit;
		outline: none;
		box-sizing: border-box;
		overflow: scroll;
	}

	:global(.note-footer) {
		flex-basis: 50px;
		/* overflow: hidden; */
		padding: 10px;
		background: inherit;
		box-sizing: border-box;
	}

	:global(.overlay-make-note) {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.8);
		backdrop-filter: blur(5px);
		z-index: 2000;
		transition: all 5s ease;
	}
</style>
