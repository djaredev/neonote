<script lang="ts">
	import Button from "$lib/components/Button.svelte";
	import Field from "$lib/components/Field.svelte";
</script>

<div class="profile">
	<label for="" class="label">Username</label>
	<Field />
	<label for="" class="label">Email</label>
	<Field />
	<Button class="button">Save</Button>
</div>

<style>
	.profile {
		display: flex;
		flex-direction: column;
		gap: 10px;
		border: 1px solid #313244;
		border-radius: 8px;
		padding: 20px;

		.label {
			color: #a6adc8;
			text-align: left;
			padding: 2px;
		}

		:global(.button) {
			align-self: end;
		}
	}
</style>
