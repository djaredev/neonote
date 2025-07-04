<script lang="ts">
	let { class: className = "", value = $bindable(), ...restProps } = $props();
</script>

<input class={["field", className]} bind:value {...restProps} />

<style>
	* {
		box-sizing: border-box;
	}
	.field {
		width: 100%;
		height: 45px;
		background: #181825;
		color: #cdd6f4;
		border-radius: 8px;
		border: 1px solid #313244;
		outline: none;
		color: #cdd6f4;
		font-size: 16px;
		padding: 10px;
	}

	.field:focus {
		border-color: #585b70;
		box-shadow: 0 0 0 4px #313244;
	}
</style>
