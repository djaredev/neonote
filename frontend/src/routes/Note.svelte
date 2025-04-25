<script lang="ts">
	import archive from "$lib/icons/archive.svg";
	import trash from "$lib/icons/trash.svg";

	let note: HTMLElement;
	let title: HTMLElement;
	let body: HTMLElement;
	let x: number, y: number, left: number, top: number;
	let isClose = $state(true);
	let editMode = $state(false);
	let resizeObserver: boolean = false;
	let trans = $state(true);
	let expanded = $state(false);

	function open() {
		console.log(note);
		console.log(title);
		const rect = note.getBoundingClientRect();

		x = (window.innerWidth - rect.width * 2.5) / 2;
		y = (window.innerHeight - rect.height) / 3;

		left = rect.left;
		top = rect.top;

		note.style.transform = `translate(${x}px, ${y}px)`;
		note.style.height = "auto";
		note.style.width = rect.width * 2.5 + "px";
		resizeObserver = true;
		// note.classList.add("expanded");
		expanded = true;
		editMode = true;
		isClose = false;
		trans = true;
	}

	function transitionend(event: TransitionEvent) {
		if (event.propertyName !== "width") return;
		console.log("transitionend");
		// resizeObserver = true;
		trans = false;
	}

	function resizeNote(height: number) {
		if (!resizeObserver) return;
		console.log("Resize observer");
		console.log(height);
		y = (window.innerHeight - height) / 3;
		note.style.transform = `translate(${x}px, ${y}px)`;
	}

	function close(event: MouseEvent) {
		if (note.contains(event.target as Node)) return;
		resizeObserver = false;
		note.style.width = note.getBoundingClientRect().width / 2.5 + "px";
		note.style.transform = `translate(${left}px, ${top}px)`;
		expanded = false;
		editMode = false;
		isClose = true;
	}
</script>

<svelte:document onclick={close} />

<div class="layout">
	<div
		class={["note", expanded && "expanded"]}
		onclick={isClose ? open : null}
		ontransitionend={trans ? transitionend : null}
		bind:this={note}
		bind:clientHeight={null, resizeNote}
	>
		<div class="note-title" contenteditable={editMode} bind:this={title}>Este es el titulo</div>
		<div class="note-body" contenteditable={editMode} bind:this={body}>
			Lorem ipsum dolor sit amet consectetur adipisicing elit. Repellendus aliquam odit, in tempore
			repudiandae ipsum perferendis alias quas quae dicta, obcaecati maiores iste vero harum error
			et, facilis debitis? Eaque?
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
</div>

<style>
	.layout {
		position: relative;
		width: 100%;
		height: 100vh;
		/* background: #11111b; */
		border: none;
		padding: 0;
		margin: 0;
	}

	.note {
		position: absolute;
		display: flex;
		flex-direction: column;
		width: 240px;
		max-height: 590px;
		color: white;
		background: #11111b;
		border: 1px solid #313244;
		border-radius: 5%;
		overflow: hidden;
		transition: all 0.14s ease;
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
		z-index: 1000;
		/* transition: all 0.3s ease; */
		user-select: none;
		font-size: 1rem;
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

		~ .overlay {
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

	.overlay {
		position: fixed;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.5);
		opacity: 0;
		pointer-events: none;
		transition: all 0.3s ease;
	}

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
</style>
