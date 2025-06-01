<script lang="ts">
	import archive from "$lib/icons/archive.svg";
	import trash from "$lib/icons/trash.svg";
	import { fade } from "svelte/transition";
	import { Modal } from "$lib/components/Modal";
	import TextEditor from "$lib/components/Editor/TextEditor.svelte";

	let title = $state("");
	let content = $state("");

	function customCenter(width: number, height: number) {
		return {
			left: (window.innerWidth - width) / 2,
			top: (window.innerHeight - height) / 3
		};
	}

	let transition = {
		type: fade,
		duration: { duration: 200 }
	};
</script>

<Modal.Root class="make-note" {customCenter}>
	<Modal.Preview class="make-note-preview">
		<div class="placeholder">Take a note...</div>
	</Modal.Preview>
	<Modal.Overlay class="overlay-view" {transition} />
	<Modal.View class="make-note-view">
		<TextEditor class="note-title-expand" bind:value={title} placeholder="Title" />
		<TextEditor class="note-body-expand" bind:value={content} placeholder="Take a note..." />
		<div class="note-footer">
			<div class="note-options">
				<button>
					<img src={archive} alt="" />
				</button>
				<button>
					<img src={trash} alt="" />
				</button>
			</div>
		</div>
	</Modal.View>
</Modal.Root>

<!-- <NoteTwo /> -->

<style>
	:global(.make-note) {
		align-self: center;
	}

	:global(.placeholder) {
		font-size: 16px;
		opacity: 0.6;
		padding-left: 15px;
	}

	:global(.make-note-preview) {
		/* position: absolute; */
		display: flex;
		align-items: center;
		justify-content: start;

		width: 600px;
		max-height: 450px;
		overflow: hidden;
		transition: all 0s ease;
		color: white;
		background: #11111b;
		border-radius: 8px;
		border: 1px solid #313244;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
		height: 54px;
	}

	:global(.disableAnimation) {
		transition: none;
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
		transition: all 0.12s ease;
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
