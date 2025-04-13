<!-- File: tests/sample_web_files/svelte/Component.svelte -->

<script>
  export let name = 'world';
  let count = 0;
  
  function handleClick() {
    count += 1;
  }
</script>

<main>
  <h1>Hello {name}!</h1>
  <button on:click={handleClick}>
    Clicked {count} {count === 1 ? 'time' : 'times'}
  </button>
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }
  
  h1 {
    color: #ff3e00;
    font-size: 4em;
    font-weight: 100;
  }
  
  button {
    background-color: #ff3e00;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 4px;
  }
</style>