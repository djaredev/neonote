<script lang="ts">
	import archive from "$lib/icons/archive.svg";
	import trash from "$lib/icons/trash.svg";
	import { notes } from "$lib/state/note.svelte";
	import { deleteNote, updateNote } from "@neonote/sdk";

	let { masonry, num, title, content } = $props();
	let noteHeight: number;
	let noteWidth: number = $state(0);
	let innerWidth: number = $state(0);
	let innerHeight: number = $state(0);
	let left: string = $state("");
	let top: string = $state("");
	let position: string = $state("obsolute");
	let isClose: boolean = $state(true);
	let editMode: boolean = $state(false);
	let transition: boolean = $state(false);
	let expanded: boolean = $state(false);
	let zIndex: boolean = $state(false);
	let disableAnimation: boolean = $state(false);
	let resizeObserver: boolean = false;
	let note: HTMLElement;
	let rect: DOMRect;
	let noteClone: HTMLElement;
	let overlay: HTMLElement = document.getElementById("overlay");

	function move(x: number, y: number) {
		left = `${x}px`;
		top = `${y}px`;
	}

	function open() {
		disableAnimation = true;
		noteClone = note.cloneNode(true) as HTMLElement;
		noteClone.style.visibility = "hidden";
		note.parentNode?.insertBefore(noteClone, note);
		noteClone.classList.add("expanded");
		const expandHeight = noteClone.offsetHeight;
		noteClone.classList.remove("expanded");
		rect = note.getBoundingClientRect();
		position = "fixed";
		move(rect.left, rect.top);

		setTimeout(() => {
			isClose = disableAnimation = false;
			transition = zIndex = expanded = editMode = true;
			move((innerWidth - noteWidth * 2.5) / 2, (innerHeight - expandHeight) / 3);
			overlay.classList.add("active");
		}, 100);
	}

	function transitionend(event: TransitionEvent) {
		if (!isClose && event.propertyName === "width") {
			transition = false;
			document.body.appendChild(note);
			resizeObserver = true;
		} else if (isClose && event.propertyName === "font-size") {
			zIndex = transition = false;
			disableAnimation = true;
			position = "absolute";
			move(noteClone.offsetLeft, noteClone.offsetTop);
			noteClone.remove();
			setTimeout(() => {
				disableAnimation = false;
			}, 0);
			masonry();
		}
	}

	function resizeHeight(clientHeight: number) {
		noteHeight = clientHeight;
		if (!resizeObserver) return;
		top = (innerHeight - noteHeight) / 3 + "px";
	}

	function close(event: MouseEvent) {
		if (note.contains(event.target as Node)) return;
		console.log(title);
		expanded = editMode = resizeObserver = false;
		isClose = transition = true;
		noteClone.parentNode?.insertBefore(note, noteClone);
		rect = noteClone.getBoundingClientRect();
		overlay.classList.remove("active");
		move(rect.left, rect.top);
		save();
	}

	function onresize() {
		if (!resizeObserver) return;
		move((window.innerWidth - noteWidth) / 2, (window.innerHeight - noteHeight) / 3);
		if (noteHeight > innerHeight) {
			note.style.height = "100vh";
		} else if (noteHeight + 25 < innerHeight) {
			note.style.height = "auto";
		}
	}

	async function save() {
		let note = notes.notes.find((note) => note.id == num);
		if (note && (note.title !== title || note.content !== content)) {
			const res = await updateNote({
				body: {
					title: title,
					content: content
				},
				path: {
					id: num
				}
			});
			if (res.data) {
				// setTimeout(() => {
				// 	notes.notes = notes.notes.filter((note) => note.id !== num);
				// 	setTimeout(() => {
				// 		notes.notes.unshift(res.data);
				// 	}, 200);
				// 	console.log("Note updated!");
				// }, 200);

				console.log("Note updated!");
			}
		}
	}

	async function remove(event: MouseEvent) {
		event.stopPropagation();
		const res = await deleteNote({
			path: {
				id: num
			}
		});
		if (res.data) {
			console.log("Note deleted!");
			notes.notes = notes.notes.filter((note) => note.id !== num);
		}
	}
</script>

<svelte:window {onresize} bind:innerWidth bind:innerHeight />
<svelte:document onclick={!isClose && !transition ? close : null} />
<div
	class={["note", { expanded, zIndex, disableAnimation }]}
	onclick={isClose && !transition ? open : null}
	ontransitionend={transition ? transitionend : null}
	bind:this={note}
	bind:clientWidth={noteWidth}
	bind:clientHeight={null, resizeHeight}
	style:position
	style:top
	style:left
	id="note-{num}"
>
	{#if editMode}
		<div class="note-title" contenteditable="true" bind:textContent={title}></div>
		<div class="note-body" contenteditable="true" bind:textContent={content}></div>
	{:else}
		<div class="note-title">{title}</div>
		<div class="note-body">{content}</div>
	{/if}
	<div class="note-footer">
		<div class="note-options">
			<button>
				<img src={archive} alt="" />
			</button>
			<button>
				<img onclick={remove} src={trash} alt="" />
			</button>
		</div>
	</div>
</div>

<style>
	/* .layout { */
	/* 	position: relative; */
	/* 	width: 100%; */
	/* 	height: 100vh; */
	/* 	background: #11111b; */
	/* 	border: none; */
	/* 	padding: 0; */
	/* 	margin: 0; */
	/* } */

	.note {
		position: absolute;
		display: flex;
		flex-direction: column;
		width: 240px;
		/* min-width: 100px; */
		max-height: 590px;
		color: white;
		background: #11111b;
		border: 1px solid #313244;
		border-radius: 10px;
		overflow: hidden;
		transition: all 0.12s ease;
		/* transition: */
		/* 	transform 0.12s ease, */
		/* 	height 0.12s ease, */
		/* 	width 0.12s ease, */
		/* 	padding 0.12s ease, */
		/* 	font-size 0.12s ease; */
		/* transform 5s ease, */
		/* width 5s ease, */
		/* height 5s ease; */
		user-select: none;
		font-size: 0.875rem;
		box-sizing: border-box;

		&:hover .note-options {
			opacity: 1;
		}
	}

	.disableAnimation {
		/* transition: all 0.12s ease; */
		transition: none;
	}

	.expanded {
		/* transition: all 0.3s ease; */
		position: fixed;
		user-select: none;
		font-size: 1rem;
		width: 600px;
		max-height: 824px;
		z-index: 1000;

		.note-title {
			padding: 15px;
			font-weight: bold;
			overflow: scroll;
			/* font-size: 15px; */
		}
		.note-body {
			padding: 15px;
			overflow: scroll;
			/* font-size: 15px; */
		}

		/* ~ .overlay { */
		/* 	opacity: 1; */
		/* 	pointer-events: all; */
		/* } */
		/* :global(~ .overlay) { */
		/* 	opacity: 1; */
		/* 	pointer-events: all; */
		/* } */

		/* .note-options { */
		/*   & img { */
		/*     width: 16px; */
		/*     height: 16px; */
		/*   } */
		/* } */
	}

	.zIndex {
		z-index: 1000;
	}

	.note-title {
		padding: 10px;
		min-height: 50px;
		max-height: 100px;
		font-weight: bold;
		background: inherit;
		outline: none;
		box-sizing: border-box;
	}

	.note-body {
		/* flex-basis: 30px; */
		flex-grow: 1;
		overflow: hidden;
		/* overflow: scroll; */
		/* max-height: 300px; */
		/* white-space: pre-wrap; */
		padding: 10px;
		background: inherit;
		outline: none;
		box-sizing: border-box;
	}

	.note-footer {
		flex-basis: 50px;
		/* overflow: hidden; */
		padding: 10px;
		background: inherit;
		box-sizing: border-box;
	}

	/* :global { */
	/* 	~ .overlay { */
	/* 		position: fixed; */
	/* 		width: 100%; */
	/* 		height: 100%; */
	/* 		background-color: rgba(0, 0, 0, 0.5); */
	/* 		opacity: 0; */
	/* 		pointer-events: none; */
	/* 		transition: all 0.3s ease; */
	/* 	} */
	/* } */

	.note-options {
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

	@media (width <= 600px) {
		.expanded {
			width: 100%;
		}
	}
</style>
