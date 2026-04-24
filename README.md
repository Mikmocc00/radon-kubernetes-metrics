# Kubernetes Manifest Metrics — IaC Defect Prediction

Questa libreria estrae metriche statiche da manifest Kubernetes (YAML/JSON) per supportare modelli di **within-repo IaC defect prediction**.

---

## Metriche disponibili

### 1. `AvgContainersPerPod`

**Tipo:** `float`

Calcola il numero medio di container definiti all'interno di ciascun Pod (o template di Pod in risorse come Deployment, StatefulSet, ecc.).

**Perché è importante:** Un numero elevato di container per Pod spesso indica una violazione del pattern "one-process-per-container" o un uso eccessivo di sidecar. Pod troppo complessi consumano più risorse, complicano il networking interno e sono più soggetti a fallimenti a cascata. Nei modelli ML, picchi in questa metrica sono spesso correlati a difetti architetturali e di scheduling.

---

### 2. `AvgFieldsPerResource`

**Tipo:** `float`

Calcola il numero medio di campi (chiavi YAML/JSON) per ogni risorsa definita nel manifest.

**Perché è importante:** È un indicatore diretto della verbosità e della granularità della configurazione. Risorse con un numero di campi anomalo (troppo alto) tendono a essere over-ingegnerizzate o a contenere configurazioni ridondanti, aumentando il carico cognitivo per i manutentori e la probabilità di errori di battitura o misconfigurazioni logiche.

---

### 3. `AvgResourceSize`

**Tipo:** `int`

Calcola la dimensione media in righe (Line of Code, escludendo quelle vuote) per singola risorsa K8s all'interno del manifest.

**Perché è importante:** Simile alla metrica `DockerfileLines`, la dimensione del blocco di codice è un predittore universale di difettosità nel software. Manifest immensi sono difficili da ispezionare durante le code review. I modelli di ML usano questa metrica per identificare risorse monolitiche che andrebbero frammentate usando tool come Helm o Kustomize.

---

### 4. `ConfigEntropy`

**Tipo:** `float`

Calcola l'entropia di Shannon basata sulla frequenza dei token all'interno dei valori del manifest.

**Perché è importante:** L'entropia misura il "disordine" o l'imprevedibilità del contenuto. Un'entropia molto alta indica un vocabolario estremamente variegato, spesso sintomo di scarsa standardizzazione, assenza di convenzioni di naming coerenti o abuso di configurazioni custom hardcodate. I modelli ML la utilizzano per rilevare manifest "atipici" rispetto al resto del repository.

---

### 5. `ManifestStructuralComplexity`

**Tipo:** `int`

Calcola la complessità strutturale totale moltiplicando il numero di campi totali per il numero di risorse nel manifest.

**Perché è importante:** Fornisce uno score globale della "superficie di errore" dell'intero file. Combina l'estensione (quante risorse) con la densità (quanti campi). Un aumento improvviso di questa metrica in una Pull Request è un forte segnale di allarme per potenziali regressioni IaC.

---

### 6. `MaxSpecDepth`

**Tipo:** `int`

Calcola la profondità massima di annidamento degli oggetti (dict/list) all'interno delle chiavi `spec`.

**Perché è importante:** Configurazioni profondamente annidate sono intrinsecamente difficili da leggere e facili da sbagliare, specialmente in YAML dove l'indentazione è semantica. Una profondità eccessiva spesso porta a difetti dovuti a errori di indentazione (es. un blocco applicato a un livello sbagliato) che passano le validazioni sintattiche ma falliscono a livello logico.

---

### 7. `NestedObjectRatio`

**Tipo:** `float`

Rapporto tra il numero di campi che contengono strutture annidate (liste o dizionari) e il totale dei campi.

**Perché è importante:** Indica la proporzione di configurazioni "complesse" rispetto a quelle "piatte" (chiave-valore semplice). Un rapporto sbilanciato verso oggetti annidati caratterizza risorse con configurazioni avanzate (es. volumi complessi, regole di rete, affinità) che statisticamente presentano un tasso di difettosità maggiore rispetto a deployment banali.

---

### 8. `NumAffinityRules`

**Tipo:** `int`

Conta il numero di blocchi `affinity` (nodeAffinity, podAffinity, podAntiAffinity) definiti nelle specifiche.

**Perché è importante:** Le regole di affinità sono potenti ma notoriamente fragili. Configurazioni errate possono impedire lo scheduling dei Pod (es. deadlock tra anti-affinità) o concentrare il carico su pochi nodi. Nei modelli di defect prediction, un alto numero di queste regole aumenta esponenzialmente il rischio di difetti legati all'allocazione delle risorse (scheduling failures).

---

### 9. `NumAnnotations`

**Tipo:** `int`

Conta il numero totale di annotazioni (`annotations`) nelle `metadata`.

**Perché è importante:** Le annotazioni vengono spesso abusate per passare configurazioni implicite a Ingress controller, Service Mesh o tool esterni. Un numero eccessivo indica un forte accoppiamento con l'infrastruttura sottostante o "logica ombra" non validata dallo schema nativo di Kubernetes. È fonte frequente di errori silenti.

---

### 10. `NumCapabilitiesAdded`

**Tipo:** `int`

Conta quanti container o initContainer aggiungono funzionalità del kernel esplicite tramite `securityContext.capabilities.add`.

**Perché è importante:** Aggiungere capabilities espande la superficie di attacco del container aggirando alcune restrizioni di default. Sebbene a volte necessario, è un indicatore diretto di complessità legata alla sicurezza e ai permessi. Spesso i difetti emergono quando i container vengono spostati in namespace con PodSecurityPolicies/Admission Controllers più rigidi.

---

### 11. `NumConfigMaps`

**Tipo:** `int`

Conta il numero di risorse di tipo `ConfigMap`.

**Perché è importante:** Contribuisce a delineare l'architettura del manifest. Un numero elevato può indicare una configurazione frammentata o un'eccessiva iniezione di script applicativi tramite IaC, una pratica che spesso porta a disallineamenti tra l'ambiente e l'applicazione.

---

### 12. `NumContainers`

**Tipo:** `int`

Conta il totale assoluto di container definiti nel manifest.

**Perché è importante:** È una proxy della dimensione del workload applicativo distribuito dal manifest. Come per la dimensione del file, più container implicano più configurazioni di rete, storage e risorse, alzando proporzionalmente la probabilità di introdurre difetti.

---

### 13. `NumDeprecatedAPIVersions`

**Tipo:** `int`

Conta quante risorse utilizzano versioni delle API obsolete come `v1beta1`, `v1alpha1` o `extensions/`.

**Perché è importante:** È una metrica critica per la manutenibilità e la stabilità. Usare API deprecate è un difetto latente (technical debt) che esploderà non appena il cluster verrà aggiornato a versioni più recenti di K8s (es. la rimozione delle API `v1beta1` in K8s 1.22).

> Il valore deve essere rigorosamente `0` per cluster moderni.

---

### 14. `NumDuplicateNames`

**Tipo:** `int`

Conta quante risorse condividono l'esatto valore in `metadata.name`.

**Perché è importante:** In K8s, risorse dello stesso tipo nello stesso namespace non possono avere lo stesso nome, ma tipi diversi sì (es. un Deployment e un Service). Sebbene sia una pratica comune usare lo stesso nome per correlazione logica, troppi duplicati aumentano le collisioni se l'utente sbaglia il `kind`, causando overwrite imprevisti. Può predire difetti di sovrascrittura logica.

---

### 15. `NumHardcodedValues`

**Tipo:** `int`

Conta le variabili d'ambiente (`env`) che definiscono un `value` statico senza usare meccanismi dinamici come `valueFrom` (SecretKeyRef / ConfigMapKeyRef).

**Perché è importante:** Come nel caso degli IP hardcodati, valori statici rendono il manifest rigido e non riutilizzabile tra ambienti diversi (es. dev/staging/prod). Può indicare anti-pattern di configurazione e potenziali difetti di deploy quando il manifest viene promosso ad ambienti superiori.

---

### 16. `NumHostIPC`

**Tipo:** `int`

Conta quante specifiche di Pod abilitano l'accesso allo spazio IPC dell'host (`hostIPC: true`).

**Perché è importante:** Indicatore critico di vulnerabilità di sicurezza. Consente ai container di comunicare con i processi dell'host, facilitando attacchi di container breakout. In modelli di IaC defect prediction legati alla sicurezza, è uno dei segnali più allarmanti.

> Il valore deve essere `0`.

---

### 17. `NumHostNetwork`

**Tipo:** `int`

Conta quante specifiche di Pod richiedono la rete dell'host (`hostNetwork: true`).

**Perché è importante:** Annulla l'isolamento di rete fornito da K8s. Il container espone le porte direttamente sull'IP del nodo e può intercettare il traffico di rete del nodo. Spesso porta a conflitti di porta (Port Bind errors) e difetti di affidabilità se più Pod vengono schedulati sullo stesso nodo.

> Il valore deve essere `0`.

---

### 18. `NumHostPID`

**Tipo:** `int`

Conta quante specifiche di Pod richiedono l'accesso allo spazio dei processi dell'host (`hostPID: true`).

**Perché è importante:** Metrica di sicurezza critica. Permette al container di vedere e manipolare i processi del nodo host (incluso kubelet). Fortemente correlato a configurazioni malevole o tool di monitoring estremamente invasivi, la cui configurazione è prona a causare instabilità nel cluster.

> Il valore deve essere `0`.

---

### 19. `NumImagePullPolicyAlways`

**Tipo:** `int`

Conta quanti container hanno la policy impostata su `Always`.

**Perché è importante:** Se da un lato garantisce di scaricare l'ultima versione dell'immagine, dall'altro introduce forti inefficienze (tempi di deploy lunghi), consuma banda e rende il cluster vulnerabile a downtime temporanei del registry delle immagini. Può predire timeout o `ImagePullBackOff` intermittenti.

---

### 20. `NumImages`

**Tipo:** `int`

Conta il numero totale di immagini dichiarate.

**Perché è importante:** Indica quante dipendenze esterne al cluster sono necessarie per instanziare il manifest. Un alto numero di immagini distinte aumenta le probabilità di fallimenti legati alla supply chain del software o ad artifact registry irraggiungibili.

---

### 21. `NumIngresses`

**Tipo:** `int`

Conta le risorse di tipo `Ingress`.

**Perché è importante:** L'Ingress è una delle risorse più complesse da configurare in K8s (annotazioni specifiche, routing, regole TLS). La sua presenza segnala l'esposizione dell'applicativo verso l'esterno. Manifest che contengono Ingress hanno statisticamente un tasso di difetti legati a misconfigurazioni di rete, DNS o certificati molto più alto.

---

### 22. `NumInitContainers`

**Tipo:** `int`

Conta il numero totale di `initContainers`.

**Perché è importante:** Gli initContainer eseguono operazioni di setup sequenziali bloccanti prima dell'avvio dell'app. Un uso estensivo indica dipendenze complesse di avvio (es. attendere DB, copiare asset). Se falliscono o vanno in timeout, l'intero Pod resta in `Init:CrashLoopBackOff`. È un eccellente predittore di difetti legati a startup falliti.

---

### 23. `NumKinds`

**Tipo:** `int`

Conta quante tipologie uniche di risorse K8s (es. Deployment, Service, Role) sono usate nel manifest.

**Perché è importante:** Misura la "larghezza" architetturale. Un manifest che aggrega molti Kinds diversi implementa applicazioni complesse (es. un intero stack con RBAC, Storage, Networking, Workload). Modelli ML sfruttano questa metrica per categorizzare il dominio del manifest.

---

### 24. `NumLabels`

**Tipo:** `int`

Conta il numero totale di etichette (`labels`) applicate.

**Perché è importante:** Le label regolano il routing dei servizi e le query dei selettori in K8s. Poche label rendono l'osservabilità povera; configurazioni complesse (troppe label) aumentano il rischio che un Service o un NetworkPolicy manchi i target desiderati a causa di un selettore non combaciante.

---

### 25. `NumLatestTag`

**Tipo:** `int`

Conta i container che utilizzano il tag `:latest` (o omettono il tag).

**Perché è importante:** L'equivalente K8s della metrica `UsesLatestTag` del Dockerfile. L'uso di `:latest` rende l'ambiente effimero, non predicibile e causa l'impossibilità di fare rollback deterministici (poiché l'immagine cambia senza variare la configurazione YAML). Fortissimo predittore di deployment buggati in produzione.

> Il valore ideale è `0`.

---

### 26. `NumLivenessProbes`

**Tipo:** `int`

Conta i container che definiscono un `livenessProbe`.

**Perché è importante:** La liveness probe indica a K8s se riavviare un container bloccato. La presenza di questa configurazione denota maturità, tuttavia una liveness configurata male (es. timeout troppo bassi) causa continui riavvii a catena (`CrashLoopBackOff`). In defect prediction, bilancia la metrica delle probe mancanti.

---

### 27. `NumMissingProbes`

**Tipo:** `int`

Conta i container in cui mancano del tutto sonde di stato (`livenessProbe`, `readinessProbe`, `startupProbe`).

**Perché è importante:** I container senza sonde non sono in grado di gestire picchi di traffico o blocchi applicativi in modo autonomo: K8s non saprà mai quando l'app è pronta o se ha smesso di rispondere, inoltrando traffico verso Pod "zombie". È un chiaro indicatore di manifest non adatti ad ambienti di produzione.

> Il valore ideale è `0` in produzione.

---

### 28. `NumMissingResources`

**Tipo:** `int`

Conta i container a cui non sono applicati vincoli o richieste di calcolo (`resources.limits` o `resources.requests`).

**Perché è importante:** K8s si basa su requests/limits per lo scheduling efficiente. La mancanza di requests causa assegnazioni sub-ottimali; la mancanza di limits permette ai container di cannibalizzare la CPU/RAM del nodo portando a OOMKilled a cascata (Out Of Memory). È uno dei principali difetti di affidabilità in K8s.

> Il valore ideale è `0`.

---

### 29. `NumNodePorts`

**Tipo:** `int`

Conta i Service configurati esplicitamente con `type: NodePort`.

**Perché è importante:** Il NodePort espone una porta direttamente sull'IP pubblico/privato di ogni nodo del cluster. Rispetto a un LoadBalancer o un Ingress, è spesso un pattern di rete legacy o debole. Aumenta la superficie di attacco del cluster host e crea dipendenze hardware rigide, causando difetti di disponibilità in ambienti dinamici.

### 30. `NumNodeSelectors`

**Tipo:** `int`

Conta il numero di chiavi definite nel blocco `nodeSelector` di ciascun Pod.

**Perché è importante:** Il `nodeSelector` forza lo scheduling dei Pod su nodi con specifiche etichette. Configurazioni troppo restrittive, o etichette digitate male, causeranno lo stallo del Pod in stato `Pending` (scheduling failure). Un alto numero di selettori aumenta drasticamente questo rischio.

---

### 31. `NumPersistentVolumes`

**Tipo:** `int`

Conta il totale delle risorse `PersistentVolume` (PV) e `PersistentVolumeClaim` (PVC).

**Perché è importante:** La gestione dello stato e dello storage in Kubernetes è complessa. Manifest che definiscono PV e PVC introducono rischi legati all'allocazione dinamica, alle access mode e alle policy di retention. In ambito IaC defect prediction, è un forte indicatore di complessità legata allo storage.

---

### 32. `NumPorts`

**Tipo:** `int`

Conta il numero totale di porte dichiarate nell'array `ports` dei container e initContainers.

**Perché è importante:** Un container che espone molte porte espande la propria superficie di attacco e complica il mapping della rete intra-cluster. Spesso segnala un container "fat" che gestisce troppi servizi contemporaneamente, violando le best practice di disaccoppiamento.

---

### 33. `NumPrivilegedContainers`

**Tipo:** `int`

Conta i container in cui è impostato `securityContext.privileged: true`.

**Perché è importante:** Metrica di sicurezza gravissima. Un container privilegiato ha un accesso quasi totale alle risorse dell'host sottostante, bypassando l'isolamento standard di Docker/containerd. Nei modelli ML di security defect prediction, questo è uno dei segnali di vulnerabilità più forti in assoluto.

> **Valore ideale:** `0` (salvo rarissime eccezioni a livello di sistema).

---

### 34. `NumReadinessProbes`

**Tipo:** `int`

Conta i container che definiscono una `readinessProbe`.

**Perché è importante:** La Readiness Probe determina quando un container è pronto a ricevere traffico di rete. La sua assenza causa downtime durante i rolling update (K8s invia traffico prima che l'app sia pronta), mentre una misconfigurazione può rimuovere permanentemente un Pod sano dal bilanciatore. Da confrontare con `NumMissingProbes`.

---

### 35. `NumResourceLimits` / `NumResourceRequests`

**Tipo:** `int`

Conta i blocchi `resources.limits` e `resources.requests` definiti nei container.

**Perché è importante:** Definiscono il tetto massimo e minimo (garantito) delle risorse (CPU/RAM). L'assenza di requests porta a scheduling inefficiente; l'assenza di limits permette l'abuso del nodo causando `OOMKilled`. Insieme, queste due metriche sono i predittori primari per i difetti di affidabilità e stabilità in esecuzione.

---

### 36. `NumResources`

**Tipo:** `int`

Conta il numero totale di documenti K8s (risorse indipendenti separate da `---`) nel manifest.

**Perché è importante:** È una metrica dimensionale di base. Manifest che contengono dozzine di risorse (Deployment, Service, ConfigMap, Role, ecc.) sono più difficili da analizzare e statisticamente più inclini a contenere difetti di integrazione tra le loro stesse componenti.

---

### 37. `NumRunAsRoot`

**Tipo:** `int`

Conta i container configurati esplicitamente con `securityContext.runAsUser: 0` (esecuzione come utente root).

**Perché è importante:** Eseguire applicazioni come root all'interno di un container è un ben noto anti-pattern di sicurezza. Se un attaccante compromette l'applicazione, avrà privilegi di root. Molti cluster con policy restrittive (es. OPA Gatekeeper) rifiuteranno il deploy, rendendolo un difetto bloccante.

---

### 38. `NumSecretsUsage`

**Tipo:** `int`

Conta quante volte vengono referenziati dei `Secret` tramite `envFrom.secretRef` o `env.valueFrom.secretKeyRef`.

**Perché è importante:** È una buona pratica per evitare l'hardcoding, ma un alto numero di riferimenti a Secret aumenta la dipendenza da configurazioni esterne al manifest. Se i Secret non sono pre-popolati nel cluster o c'è un refuso nel nome, il Pod andrà in crash all'avvio (`CreateContainerConfigError`).

---

### 39. `NumServices`

**Tipo:** `int`

Conta le risorse di tipo `Service` nel manifest.

**Perché è importante:** I Service regolano il networking intra-cluster. Un numero elevato indica una topologia di rete complessa, aumentando il rischio di misconfigurazioni legate ai `selector` o al mapping delle porte tra Service e Pod target.

---

### 40. `NumSpecFields` / `NumTotalFields`

**Tipo:** `int`

`NumSpecFields` conta la profondità e l'estensione totale dei campi solo sotto i blocchi `spec`, mentre `NumTotalFields` conta ogni singolo campo dell'intero manifest.

**Perché è importante:** Rappresentano la misura definitiva del "volume" della configurazione logica (Spec) e globale. Modelli ML sfruttano queste metriche come baseline di densità: un file con molti campi è, matematicamente, un file con una probabilità maggiore di contenere un errore umano.

---

### 41. `NumStartupProbes`

**Tipo:** `int`

Conta i container che definiscono una `startupProbe`.

**Perché è importante:** Usate per applicazioni legacy o particolarmente lente ad avviarsi, disabilitano le altre probe finché non hanno successo. Una startupProbe configurata con timeout errati rischia di bloccare in un limbo il container per minuti o di ucciderlo prima che abbia finito di inizializzarsi.

---

### 42. `NumTolerations`

**Tipo:** `int`

Conta il totale delle regole `tolerations` applicate ai Pod.

**Perché è importante:** Le tolerations permettono ai Pod di essere schedulati su nodi con "Taints" restrittivi. Sono meccanismi avanzati; errori nella tolleranza portano i Pod su nodi sbagliati o impediscono completamente l'allocazione, portando a difetti di operatività a livello di infrastruttura.

---

### 43. `NumVolumes`

**Tipo:** `int`

Conta i blocchi `volumes` dichiarati a livello di Pod (configmap, secret, emptyDir, hostPath, etc.).

**Perché è importante:** Gestire il file system in K8s è insidioso. Molti volumi implicano una dipendenza da percorsi file, permessi (fsGroup) e risorse esterne. Metriche alte qui si traducono spesso in difetti di tipo `CrashLoopBackOff` causati da file inesistenti o permessi negati al runtime.

---

## Riepilogo Completo (Metriche Aggiornate)

| Metrica | Tipo | Segnale critico |
|---|---|---|
| `AvgContainersPerPod` | float | Valore alto → Pod over-ingegnerizzati, fallimenti a cascata |
| `AvgFieldsPerResource` | float | Valore alto → verbosità e probabili misconfigurazioni |
| `AvgResourceSize` | int | Valore alto → difficile da mantenere e analizzare |
| `ConfigEntropy` | float | Valore alto → configurazioni atipiche o caotiche |
| `ManifestStructuralComplexity`| int | Valore alto → superficie di errore estesa |
| `MaxSpecDepth` | int | Valore alto → errori di indentazione e validazione logica |
| `NestedObjectRatio` | float | Valore alto → eccesso di logica annidata |
| `NumAffinityRules` | int | Valore alto → rischio di scheduling deadlocks |
| `NumAnnotations` | int | Valore alto → accoppiamento infrastrutturale implicito |
| `NumCapabilitiesAdded` | int | Qualsiasi valore > 0 → rischio di sicurezza (privilegi kernel) |
| `NumConfigMaps` | int | Valore alto → configurazione frammentata |
| `NumContainers` | int | Valore alto → maggiore complessità globale |
| `NumDeprecatedAPIVersions` | int | Qualsiasi valore > 0 → debito tecnico, break all'upgrade cluster |
| `NumDuplicateNames` | int | Valore alto → rischio overwrite accidentale |
| `NumHardcodedValues` | int | Valore alto → deployment rigido e non portabile |
| `NumHostIPC/Network/PID` | int | Qualsiasi valore > 0 → rischio sicurezza critico (Node breakout) |
| `NumImagePullPolicyAlways` | int | Valore alto → inefficienza rete, latenza di deploy |
| `NumImages` | int | Valore alto → eccessiva dipendenza da registry esterni |
| `NumIngresses` | int | Valore alto → esposizione complessa, rischio routing DNS/TLS |
| `NumInitContainers` | int | Valore alto → rischio timeout in sequenza di startup |
| `NumKinds` | int | Valore alto → ampiezza architetturale elevata |
| `NumLabels` | int | Valori anomali → problemi di routing o observability |
| `NumLatestTag` | int | Qualsiasi valore > 0 → deployment non riproducibile (break improvvisi) |
| `NumNodeSelectors` | int | Valore alto → vincoli rigidi, rischio Pod `Pending` |
| `NumPersistentVolumes` | int | Valore alto → complessità di storage, potenziale data-loss |
| `NumPorts` | int | Valore alto → ampia superficie d'attacco, accoppiamento |
| `NumPrivilegedContainers` | int | Qualsiasi valore > 0 → rischio sicurezza massimo (Root host) |
| `NumReadinessProbes` | int | Assenza → rischio di instradamento verso Pod non pronti |
| `NumLiveness/StartupProbes` | int | Valore alto → bilancia l'assenza, ma rischia loop di riavvio |
| `NumMissingProbes` | int | Qualsiasi valore > 0 → inaffidabilità operativa |
| `NumMissingResources` | int | Qualsiasi valore > 0 → Node starvation (OOMKilled) |
| `NumResourceLimits/Requests`| int | Metriche base di affidabilità, mitigano i rischi di cui sopra |
| `NumResources` | int | Valore alto → manifest K8s troppo denso o monolitico |
| `NumRunAsRoot` | int | Qualsiasi valore > 0 → vulnerabilità ai container breakout |
| `NumSecretsUsage` | int | Valore alto → rischio di dipendenze runtime non soddisfatte |
| `NumServices` | int | Valore alto → topologia di rete frammentata |
| `NumSpecFields/TotalFields` | int | Indicatori base del volume logico del file (stile LOC) |
| `NumTolerations` | int | Valore alto → complessità in interazione con i nodi |
| `NumVolumes` | int | Valore alto → dipendenze fs/hardware, crash di I/O |