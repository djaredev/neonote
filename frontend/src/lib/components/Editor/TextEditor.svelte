<script lang="ts">
	import { onMount } from "svelte";
	let { class: style, value = $bindable(), placeholder } = $props();
	let innerText: string = $state(value);
	let element: HTMLElement;

	function oninput() {
		if (innerText === "\n" || innerText === "") {
			innerText = "";
		}
	}

	onMount(() => {
		oninput();
	});

	function getInnerText() {
		return innerText;
	}

	function setInnerText(text: string) {
		innerText = text;
		value = extractPlainText(element.innerHTML);
		// console.log("\n----");
		// console.log(JSON.stringify(text));
		// console.log(JSON.stringify(text.replace(/\n\n/g, "\n")));
		// console.log(JSON.stringify(element.innerHTML));
		// console.log(JSON.stringify(extractPlainText(element.innerHTML)));
	}

	function extractPlainText(html: string) {
		// Primero manejar el caso específico <div><br></div> - solo convertir a un salto
		let text = html.replace(/<div><br\s*\/?><\/div>/gi, "\n");

		// Convertir <br> y <br/> y <br /> a saltos de línea
		text = text.replace(/<br\s*\/?>/gi, "\n");

		// Convertir </div> a saltos de línea (los div suelen actuar como párrafos)
		text = text.replace(/<\/div>/gi, "\n");

		// Eliminar todas las demás etiquetas HTML
		text = text.replace(/<[^>]*>/g, "");

		// Decodificar entidades HTML comunes
		text = text.replace(/&nbsp;/g, " ");
		text = text.replace(/&amp;/g, "&");
		text = text.replace(/&lt;/g, "<");
		text = text.replace(/&gt;/g, ">");
		text = text.replace(/&quot;/g, '"');
		text = text.replace(/&#39;/g, "'");

		return text;
	}
</script>

<div
	class={["placeholder", style]}
	contenteditable="true"
	id="noteBody"
	role="textbox"
	aria-label={placeholder}
	bind:innerText={getInnerText, setInnerText}
	{oninput}
	bind:this={element}
></div>

<style>
	.placeholder:empty::before {
		content: attr(aria-label);
		color: #585b70;
	}
</style>
