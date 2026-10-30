# Copilot instructions

<!-- BEGIN:git-workspace-rules -->
## Git e workspace - regole obbligatorie per agenti LLM

1. **Cartella unica**: lavora solo in `F:\Progetti\pokémon-sicilia`. Non creare cloni, non lavorare in altre cartelle, non modificare progetti diversi da questo.
2. **Branch attivo**: `main`. Ogni modifica va committata su questo branch; il blocco `active-branch` in questo file viene aggiornato dall'hook `post-checkout`.
3. **Committa sempre tutto**: chiudi ogni task con `git add -A && git commit` sul branch attivo. Nessun lavoro non committato a fine sessione, nessuno stash lasciato in sospeso.
4. **Git flessibile**: `add`, `commit`, `switch`/`checkout`, `restore`, `stash`, `merge`, `rebase`, `tag` sono consentiti quando servono al task. Vietati: `push --force`, `reset --hard` su commit gia' pushati, `git clean -xfd` fuori da path generati.
5. **Push vietato**: nessun `git push`, nessuna PR, nessuna release o pubblicazione, se l'utente non lo chiede esplicitamente nella richiesta corrente.
6. **Messaggi di commit**: `tipo(scope): oggetto` in inglese, corpo con il perche'. Un commit per blocco logico.
7. **Segreti**: mai committare `.env`, chiavi, token o credenziali; se un file tracciato le contiene, fermati e segnala.
8. **Prima di ogni operazione Git**: `git rev-parse --abbrev-ref HEAD` e `git status --porcelain`. Se il branch non e' quello atteso, fermati e segnala.
9. **Docs sempre aggiornati**: quando l'utente cambia branch o sposta il progetto, aggiorna questo blocco (o rilancia `sync-active-branch.ps1`) nello stesso commit.
<!-- END:git-workspace-rules -->
<!-- BEGIN:active-branch -->
Branch attivo: `main` - committa qui, non cambiare branch di iniziativa.
<!-- END:active-branch -->
