using Microsoft.AspNetCore.Components.WebAssembly.Hosting;

var builder = WebAssemblyHostBuilder.CreateDefault(args);

// 🛠️ AGREGA ESTO: Registrar HttpClient para el proyecto WebAssembly (Cliente) apuntando a Python
builder.Services.AddScoped(sp => new HttpClient 
{ 
    BaseAddress = new Uri("http://localhost:8000/") 
});

await builder.Build().RunAsync();