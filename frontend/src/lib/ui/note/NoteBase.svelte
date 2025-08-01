<script>
	import { fade } from "svelte/transition";
	import { Modal } from "$lib/components/Modal";
	import TextEditor from "$lib/components/Editor/TextEditor.svelte";
	import { getNoteState } from "$lib/state/note.svelte";

	let { id, options, onClose = null, view = null } = $props();

	let note = getNoteState().findById(id);

	let transition = {
		type: fade,
		duration: { duration: 100 }
	};
</script>

{#if note}
	<Modal.Root class="note" {onClose}>
		<Modal.Preview class="preview">
			<div class="note-title" contenteditable="false" bind:innerText={note.title}></div>
			<div class="note-body" contenteditable="false" bind:innerText={note.content}></div>
			<div class="note-footer">
				<div class="note-options">
					{@render options()}
				</div>
			</div>
		</Modal.Preview>
		<Modal.Overlay class="overlay-view" {transition} />
		<Modal.View class="view">
			{#if view}
				{@render view(note)}
			{:else}
				<TextEditor class="note-title-expand" bind:value={note.title} placeholder="Title" />
				<TextEditor
					class="note-body-expand"
					bind:value={note.content}
					placeholder="Take a note..."
				/>
			{/if}
			<div class="note-footer">
				<div class="note-options">
					{@render options()}
				</div>
			</div>
		</Modal.View>
	</Modal.Root>
{/if}

<style>
	:global(.note) {
		position: absolute;
		transition: all 0.12s ease;
		color: #cdd6f4;
	}

	:global(.preview) {
		display: flex;
		flex-direction: column;
		width: 240px;
		max-height: 590px;
		color: inherit;
		background: #11111b;
		border: 1px solid #313244;
		border-radius: 10px;
		overflow: hidden;
		/* transition: all 0.12s ease; */
		user-select: none;
		font-size: 0.875rem;
		box-sizing: border-box;

		&:hover .note-options {
			opacity: 1;
		}
	}

	@media (width <= 500px) {
		:global(.note) {
			width: 100%;
		}

		:global(.preview) {
			width: 100%;
			max-height: 210px;

			& .note-options {
				visibility: hidden;
			}
		}
	}

	:global(.note-title) {
		color: inherit;
		font-size: 16px;
		padding: 10px;
		min-height: 50px;
		max-height: 100px;
		font-weight: bold;
		background: inherit;
		outline: none;
		box-sizing: border-box;
	}

	:global(.note-body) {
		color: inherit;
		flex-grow: 1;
		overflow: hidden;
		padding: 10px;
		background: inherit;
		outline: none;
		box-sizing: border-box;
	}

	/* View */
	:global(.view) {
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
		z-index: 1010;

		&:hover .note-options {
			opacity: 1;
		}
	}

	@media (width <= 600px) {
		:global(.view) {
			max-width: 100%;
			max-height: 412px;

			& .note-options {
				visibility: visible;
				opacity: 1;
			}
		}
	}

	:global(.note-title-expand) {
		color: #cdd6f4;
		font-size: 18px;
		padding: 15px;
		min-height: 50px;
		max-height: 100px;
		font-weight: bold;
		background: inherit;
		outline: none;
		box-sizing: border-box;
		overflow: scroll;
		cursor: text;
	}

	:global(.note-body-expand) {
		color: #cdd6f4;
		flex-grow: 1;
		padding: 15px;
		background: inherit;
		outline: none;
		box-sizing: border-box;
		overflow: scroll;
		cursor: text;
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
		z-index: 1010;
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

		:global(& button) {
			border: none;
			background: none;
			cursor: pointer;

			:global(& img) {
				width: 24px;
				height: 24px;
			}
		}
	}
</style>
