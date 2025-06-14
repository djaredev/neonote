<script lang="ts">
	import { fade } from "svelte/transition";
	import { Modal } from "$lib/components/Modal";
	import TextEditor from "$lib/components/Editor/TextEditor.svelte";
	import { ArchiveIcon, Trash2Icon } from "@lucide/svelte";
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
</script>

<Modal.Root class="make-note" {customCenter} {onClose}>
	<Modal.Preview class={className}>
		{@render children()}
	</Modal.Preview>
	<Modal.Overlay class="overlay-view" {transition} />
	<Modal.View class="make-note-view">
		<TextEditor class="note-title-expand" bind:value={note.title} placeholder="Title" />
		<TextEditor class="note-body-expand" bind:value={note.content} placeholder="Take a note..." />
		<div class="note-footer">
			<div class="note-options">
				<button>
					<ArchiveIcon color="#cdd6f4" />
				</button>
				<button>
					<Trash2Icon color="#cdd6f4" />
				</button>
			</div>
		</div>
	</Modal.View>
</Modal.Root>

<!-- <NoteTwo /> -->

<style>
	:global(.make-note) {
		/* align-self: center; */
	}

	:global(.make-note-preview) {
		color: #cdd6f4;
		display: flex;
		text-decoration: none;
		width: 100%;
		block-size: 50px;
		align-items: center;
		gap: 20px;
		outline: 2px solid transparent;
		border-radius: 10px;
		padding: 10px;
		box-sizing: border-box;
		/* border: 1px solid white; */
		/* overflow: hidden; */

		z-index: 1;
	}

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
		z-index: 1000;

		&:hover .note-options {
			opacity: 1;
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

	:global(.overlay-view) {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.8);
		backdrop-filter: blur(5px);
		/* display: flex; */
		/* align-items: center; */
		/* justify-content: center; */
		/* z-index: 1000; */
		/* opacity: 1; */
		/* visibility: hidden; */
		transition: all 5s ease;
	}

	:global(.note-options) {
		display: flex;
		justify-content: end;
		width: 100%;
		height: 100%;
		gap: 5px;
		font-size: 14px;
		opacity: 0;
		transition: opacity 0.3s ease-in-out;

		& button {
			border: none;
			background: none;
			cursor: pointer;

			& img {
				width: 24px;
				height: 24px;
			}
		}
	}
</style>
