let scene = new THREE.Scene();
scene.background = new THREE.Color(0xf0f8ff);

let camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 1000);
camera.position.set(0, 1.5, 3);

let renderer = new THREE.WebGLRenderer({
    canvas: document.getElementById("scene3d"),
    antialias: true
});

renderer.setSize(window.innerWidth * 0.9, 600);
renderer.shadowMap.enabled = true;

// Luces
let hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 1.2);
scene.add(hemiLight);

let dirLight = new THREE.DirectionalLight(0xffffff, 1);
dirLight.position.set(5,10,7);
scene.add(dirLight);

// Controles
let controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// Cargar modelo
let loader = new THREE.GLTFLoader();
let model;

loader.load('/static/models/human_body.glb', function(gltf){
    model = gltf.scene;
    model.scale.set(1,1,1);
    scene.add(model);
});

// Animación
function animate(){
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();

// Detectar clic
let raycaster = new THREE.Raycaster();
let mouse = new THREE.Vector2();

window.addEventListener("click", function(event){
    if(!model) return;

    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    let intersects = raycaster.intersectObjects(model.children, true);

    if(intersects.length > 0){
        let partName = intersects[0].object.name;
        mostrarHistorial(partName);
    }
});

function mostrarHistorial(parte){
    let contenido = "";

    historial.forEach(p => {
        if(p.parte.toLowerCase() === parte.toLowerCase()){
            contenido += `
                <div>
                    <h4>${p.nombre} (${p.edad})</h4>
                    <p><b>Ocupación:</b> ${p.ocupacion}</p>
                    <p><b>Diagnóstico:</b> ${p.diagnostico}</p>
                    <img src="/static/uploads/${p.imagen}" width="200">
                </div>
            `;
        }
    });

    document.getElementById("contenido").innerHTML =
        contenido || "<p>No hay registros en esta zona.</p>";

    document.getElementById("modal").style.display = "block";
}

function cerrarModal(){
    document.getElementById("modal").style.display = "none";
}