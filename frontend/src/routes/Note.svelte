<script lang="ts">
	import archive from "$lib/icons/archive.svg";
	import trash from "$lib/icons/trash.svg";

	let { masonry, num } = $props();
	let noteHeight: number;
	let noteWidth: number = $state(0);
	let innerWidth: number = $state(0);
	let innerHeight: number = $state(0);
	let isClose = $state(true);
	let editMode = $state(false);
	let transition = $state(false);
	let expanded = $state(false);
	let zIndex = $state(false);
	let note: HTMLElement;
	let title: HTMLElement;
	let body: HTMLElement;
	let x: number = $state(0);
	let y: number = $state(0);
	let left: number, top: number;
	let resizeObserver: boolean = false;
	let rect: DOMRect;

	function open() {
		rect = note.getBoundingClientRect();
		left = note.offsetLeft;
		top = note.offsetTop;
		transition = zIndex = expanded = editMode = resizeObserver = true;
		// note.style.position = "fixed";
		note.style.left = rect.left + "px";
		note.style.top = rect.top + "px";
		x = (innerWidth - rect.width * 2.5) / 2;
		y = (innerHeight - rect.height) / 3;
		x = x - rect.left;
		y = y - rect.top;

		note.style.height = "auto";
		isClose = false;
	}

	function transitionend(event: TransitionEvent) {
		if (!isClose && event.propertyName === "width") {
			transition = false;
		} else if (isClose && event.propertyName === "font-size") {
			zIndex = transition = false;
			masonry();
		}
	}

	function resizeNote(clientHeight: number) {
		noteHeight = clientHeight;
		if (!resizeObserver) return;
		y = (innerHeight - noteHeight) / 3 - rect.top;
	}

	function close(event: MouseEvent) {
		if (note.contains(event.target as Node)) return;
		expanded = editMode = resizeObserver = false;
		isClose = transition = true;
		// note.style.position = "absolute";
		note.style.left = left + "px";
		note.style.top = top + "px";
		x = y = 0;
	}

	function resize() {
		if (!resizeObserver) return;
		x = (innerWidth - noteWidth) / 2 - rect.left;
		y = (innerHeight - noteHeight) / 3 - rect.top;
		if (noteHeight > innerHeight) {
			note.style.height = "100vh";
		} else if (noteHeight + 25 < innerHeight) {
			note.style.height = "auto";
		}
	}
</script>

<!-- style:transform={`translate(${x - 60}px, ${y - 134}px)`} -->
<svelte:window bind:innerWidth bind:innerHeight onresize={resize} />
<svelte:document onclick={!isClose && !transition ? close : null} />
<div
	class={["note", expanded && "expanded", zIndex && "z-index"]}
	onclick={isClose && !transition ? open : null}
	ontransitionend={transition ? transitionend : null}
	bind:this={note}
	bind:clientWidth={noteWidth}
	bind:clientHeight={null, resizeNote}
	style:transform={`translate(${x}px, ${y}px)`}
	id="note-{num}"
>
	<div class="note-title" contenteditable={editMode} bind:this={title}>
		Este es el titulo {num}
	</div>
	<div class="note-body" contenteditable={editMode} bind:this={body}>
		Lorem ipsum dolor sit amet consectetur adipisicing elit. Repellendus aliquam odit, in tempore
		repudiandae ipsum perferendis alias quas quae dicta, obcaecati maiores iste vero harum error et,
		facilis debitis? Eaque?
	</div>
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
		transition:
			transform 0.12s ease,
			height 0.12s ease,
			width 0.12s ease,
			padding 0.12s ease,
			font-size 0.12s ease;
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

	.expanded {
		/* z-index: 1000; */
		/* transition: all 0.3s ease; */
		position: fixed;
		user-select: none;
		font-size: 1rem;
		width: 600px;
		max-height: 824px;

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
		:global(~ .overlay) {
			opacity: 1;
			pointer-events: all;
		}

		/* .note-options { */
		/*   & img { */
		/*     width: 16px; */
		/*     height: 16px; */
		/*   } */
		/* } */
	}

	.z-index {
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
