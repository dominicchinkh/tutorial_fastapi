import { homeHomeGet } from './client/sdk.gen';

async function fetchItems() {
    try {
        // Fully typed! TypeScript will know 'limit' is a number
        const items = await homeHomeGet({
        });
        
        console.log(items); // Array of your Pydantic-mapped structures

    } catch (error) {
        console.error("API error:", error);
    }
}

fetchItems();
