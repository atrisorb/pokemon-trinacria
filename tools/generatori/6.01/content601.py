"""Contenuti scritti a mano del blocco 6.01 (Prologo: il Cubbar e la casa di Corso Italia).

Qui stanno i messaggi dei tre banchi (campagna e gemello post-dimissioni), gli script `.s` con le
macro reali di HeartGold, le intestazioni degli script, gli header degli eventi, gli eventi delle
mappe (zone_event) e le righe del registro degli NPC. gen601.py li scrive nei file e controlla tutto.

Convenzioni di scrittura dei messaggi (regola R-SCR-04):
  * un messaggio e' una lista di «riquadri» separati da «¶»; ogni riquadro e' un paragrafo che
    wrap() spezza in righe da 2 (le righe di un riquadro si uniscono con \\n, i riquadri con \\f);
  * `chain=True` aggiunge un \\r finale: il messaggio e' seguito da un altro NPCMsg nello stesso
    script (come i messaggi di HeartGold che si susseguono);
  * {NOME} diventa {STRVAR_1 3, 0, 0} (nome del giocatore): lo script deve eseguire
    BufferPlayersName 0 prima del messaggio (R-TXT-07).
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
REPO = os.path.normpath(os.path.join(PROJ, '..', 'pokeheartgold'))
sys.path.insert(0, os.path.join(PROJ, 'tools'))
import trinacria_msg_lint as L  # noqa: E402

NOME = '{STRVAR_1 3, 0, 0}'
_CHARMAP = L.load_charmap(REPO)
_WIDTHS = L.load_widths(REPO)
MAX_PX = 212       # margine di 4 px sul limite di 216 (R-TXT-01)
MAX_CH = 36


def _fits(line):
    ch, px = L.measure(line, _CHARMAP, _WIDTHS)
    return ch <= MAX_CH and px <= MAX_PX


def wrap_par(par):
    """Spezza un paragrafo in righe che stanno nel riquadro (R-TXT-01)."""
    words = re.findall(r'(?:\{[^{}]*\}|[^\s{])+', par)
    lines, cur = [], ''
    for w in words:
        cand = (cur + ' ' + w) if cur else w
        if _fits(cand) or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def wrap(text, chain=False):
    """«¶» separa i riquadri; {NOME} e' il nome del giocatore. Restituisce la stringa del banco."""
    text = text.replace('{NOME}', NOME)
    boxes = []
    for par in text.split('¶'):
        lines = wrap_par(par.strip())
        for i in range(0, len(lines), 2):
            boxes.append('\n'.join(lines[i:i + 2]))
    out = '\f'.join(boxes)
    return out + ('\r' if chain else '')


def M(testo, lingua='it', area='CT', twin=None, chain=False, twin_area=None):
    """Un messaggio: testo di campagna, gemello (uguale se non indicato), lingua e area del Glossario."""
    return dict(testo=wrap(testo, chain), twin=wrap(twin if twin is not None else testo, chain),
                lingua=lingua, area=area, chain=chain, solo_campagna=twin is None)


# ----------------------------------------------------------------------------------------------
# Banco del Cubbar: msg_0603_T25SP0101, gemello msg_0870 (20 messaggi)

CUBBAR = [
    M('Misterbianco, il Cubbar.¶Le 3:30 del mattino. Il basso fa tremare i bicchieri sul banco.', chain=True),     # 00
    M('Accanto a tutti c’è un Pokémon.¶Accanto a me, solo il bicchiere.'),                                         # 01
    M('Ti presento il mio Gattupardu, {NOME}.¶Pedigree certificato: costa quanto un bilocale a Ognina.¶Il tuo dov’è?',
      twin='Il mio Gattupardu sta benissimo, {NOME}.¶Mio padre, invece, ha perso metà dello studio dopo le tue dimissioni.¶Grazie.'),   # 02
    M('Il mio Novicudi? Regalo di papà: è magistrato, sai.¶Dice che i Pokémon rari non si discutono, {NOME}.',
      twin='Papà ha riaperto un fascicolo che dormiva da anni, {NOME}.¶Dice che è merito delle tue dimissioni. Il mio Novicudi approva.'),  # 03
    M('Faccio il praticante da tre anni, {NOME}.¶Rimborso spese: un caffè e un grazie.¶Il Pokémon me lo comprerò da titolare.',
      twin='Dopo le tue dimissioni lo studio ha tagliato i praticanti, {NOME}.¶Il caffè non me lo offrono più. Complimenti.'),             # 04
    M('Sei in lista, {NOME}? No? Tranquillo.¶Basta citare il mio nome all’ingresso: il tavolo è mio.',
      twin='{NOME}! Dopo le tue dimissioni la gente balla di più.¶Giuro: serate così piene non le avevo mai viste.'),                        # 05
    M('Mio padre dice che la giustizia è lenta ma arriva.¶Mia madre dice che arriva dopo l’aperitivo, {NOME}.',
      twin='Mio padre dice che le tue dimissioni hanno rallentato tutto, {NOME}.¶Anche l’aperitivo.'),                                   # 06
    M('Mio padre fa l’imprenditore, {NOME}. Non so bene cosa.¶So che il Diavulazzu morde chi fa troppe domande.',
      twin='Dopo le tue dimissioni papà dice che le cose cambiano.¶Ha già cambiato sigla due volte, {NOME}.'),                           # 07
    M('Mbare, talìa cu c’è!', lingua='scn', chain=True),                                                           # 08
    M('Eri sparito, {NOME}. Ti cercavo da un’ora.¶Questa è la porta VIP: qui entra solo chi conosce me.', chain=True),   # 09
    M('Guardi il mio Subwoofer? Tranquillo, non morde.¶Fa solo tremare i bicchieri.', chain=True),                 # 10
    M('Senti, {NOME}: è tardi, hai una faccia da giorno dopo.¶Vai a casa e dormici sopra.', chain=True),            # 11
    M('Dumani è dumani, mbare.', lingua='scn'),                                                                    # 12
    M('Vai, {NOME}. Ci rivediamo presto, lo sento.¶Il Subwoofer ha fiuto per queste cose.'),                       # 13
    M('Il Subwoofer di Christian vibra a tempo di cassa.¶Ogni tanto sbuffa e un bicchiere trema.'),                # 14
    M('Il Gattupardu si lecca una zampa con aria da salotto.¶Ti ignora con grande eleganza.',
      twin='Il Gattupardu sbadiglia.¶Dalle tue dimissioni anche lui sembra più nervoso.'),                         # 15
    M('Il Novicudi muove le nove code a tempo di musica.¶Le luci della pista fanno il resto.',
      twin='Il Novicudi socchiude gli occhi.¶Nove code, nove opinioni diverse sulle tue dimissioni.'),             # 16
    M('Il Diavulazzu ringhia piano.¶Il collare ha una targhetta d’argento: nessun nome, solo un numero.',
      twin='Il Diavulazzu ringhia piano.¶Dalle tue dimissioni la targhetta del collare è cambiata due volte.'),    # 17
    M('Prima di uscire, due parole con Christian all’ingresso VIP.'),                                              # 18
    M('Fuori comincia a schiarire.¶La notte al Cubbar finisce qui.'),                                              # 19
]

# ----------------------------------------------------------------------------------------------
# Banco della camera: msg_0546_T20R0202, gemello msg_0851 (10 messaggi)

CAMERA = [
    M('{NOME} accende il PC e controlla la casella di posta.'),                                                    # 00
    M('Nessuna mail nuova.¶I 41 curricula inviati non hanno ancora risposto.',
      twin='Nessuna mail nuova.¶Solo tremila richieste di intervista sulle tue dimissioni.'),                                    # 01
    M('Gli scaffali sono pieni di codici LUISS: civile, penale, procedura.¶Letti tutti. Serviti a poco.',
      twin='Gli scaffali sono pieni di codici LUISS.¶Accanto, sei mesi di verbali di Palazzo d’Orléans.'),         # 02
    M('Sulla scrivania c’è una lettera col timbro del Ministero.¶Esito: “non idoneo”. Piegata in quattro.',
      twin='Sulla scrivania c’è ancora la lettera del Ministero.¶“Non idoneo”. Eppure c’è stato un Presidente.'),       # 03
    M('Il diploma del liceo Cutelli, incorniciato dalla mamma.¶La cornice ha avuto più successo di te.',
      twin='Il diploma del liceo Cutelli, incorniciato dalla mamma.¶Accanto, incorniciata, la nomina a Presidente.'),          # 04
    M('Qualche ora prima.¶Misterbianco, il Cubbar.'),                                                              # 05
    M('Ore 14:00.¶Corso Italia, camera tua.', chain=True),                                                         # 06
    M('La testa pesa ancora di basso e di luci.¶È già pomeriggio.', chain=True),                                   # 07
    M('“{NOME}!!¶Scendi subito!¶Il figlio dell’avvocato Lombardo ha già aperto lo studio a Milano!”', chain=True),  # 08
    M('Ecco. La giornata è cominciata.'),                                                                          # 09
]

# ----------------------------------------------------------------------------------------------
# Banco della casa, piano terra: msg_0545_T20R0201, gemello msg_0850 (35 messaggi).
# I messaggi 14-30 tengono la struttura del risparmio della madre di HeartGold (menu «MenuItemAdd 27..30»).

CASA = [
    M('Ben svegliato, {NOME}!¶Sono le due del pomeriggio.¶Lo hai sentito, no? Lo studio a Milano.¶A Milano, {NOME}. Capisci?', chain=True),    # 00 (ragazzo)
    M('Ben svegliata, {NOME}!¶Sono le due del pomeriggio.¶Lo hai sentito, no? Lo studio a Milano.¶A Milano, {NOME}. Capisci?', chain=True),    # 01 (ragazza)
    M('Questo è il tuo zaino. Dentro ci ho messo tre curricula e un fazzoletto.¶Non si sa mai.', chain=True),     # 02
    M('Questa è la tua tessera. C’è la tua foto.¶Ti ho fatto sistemare il ciuffo dal fotografo.', chain=True),    # 03
    M('Qui si salva tutto: i progressi, i ricordi e anche la mia fiducia, finché dura.', chain=True),             # 04
    M('E queste sono le opzioni.¶Tocca i tasti e capirai subito: hai studiato tanto, no?', chain=True),           # 05
    M('Ah, {NOME}, quasi dimenticavo!¶Ti ho ricaricato il telefono: Turi ha chiamato tre volte.', chain=True),    # 06
    M('{NOME} riceve il Pokégear!', chain=True),                                                                   # 07
    M('Il Pokégear è il telefono che ogni cittadino dovrebbe avere.¶Chiama, mostra la mappa e, se hai coraggio, anche il Sondaggio.', chain=True),  # 08
    M('Ti ricordi come si telefona? {YESNO 0}'),                                                                   # 09
    M('Allora accendi il Pokégear e tocca il tasto del telefono.', chain=True),                                    # 10
    M('Tocca Pokégear sullo schermo tattile.¶Poi tocca il tasto del telefono.', chain=True),                      # 11
    M('I nomi si registrano da soli. Scegline uno e chiama.¶E ricordati: Turi ti aspetta al Vermut, in via Gemmellaro.'),  # 12
    M('Turi ti aspetta al Vermut, in via Gemmellaro.¶Vai, almeno prendi aria.'),                                   # 13
    M('Allora te ne vai in giro per la Sicilia…¶Faccio una cosa: ogni volta che guadagni, tengo da parte una quota.¶In viaggio i soldi servono. Vuoi che li custodisca io? {YESNO 0}'),   # 14
    M('Voglio sostenerti, {NOME}, anche col Dossier in tasca.¶Ogni volta che guadagni, tengo da parte una quota.¶Vuoi che custodisca io i tuoi soldi? {YESNO 0}'),                        # 15
    M('Va bene, ci penso io ai tuoi soldi.¶Fai attenzione. I Pokémon sono amici: se fate squadra, potete tutto.¶Ora vai!'),   # 16
    M('Va bene, ma fai attenzione là fuori.¶I Pokémon sono amici: se fate squadra, potete tutto.¶Ora vai!'),     # 17
    M('Ciao! Eccoti a casa.¶Ti ho tenuto la camera in ordine.¶O forse è una questione di soldi? {YESNO 0}',
      twin='Ciao! Eccoti a casa, Presidente. Ex.¶Ti ho tenuto la camera in ordine.¶O forse è una questione di soldi? {YESNO 0}'),   # 18
    M('Fai quello che puoi.'),                                                                                     # 19
    M('Oh!¶Non hai soldi da ritirare.'),                                                                           # 20
    M('I tuoi soldi sono al sicuro qui!¶Pensa a te stesso.'),                                                      # 21
    M('{NOME}!¶Pensa bene a come li spendi!'),                                                                     # 22
    M('Vuoi mettere da parte dei soldi? {YESNO 0}'),                                                               # 23
    M('Oh!¶Non ti restano soldi da mettere da parte.¶Non sprecarli in sciocchezze, intesi?¶So che sei ragionevole come me.'),   # 24
    M('Ho messo da parte tanti soldi.¶Non posso tenerne altri.'),                                                  # 25
    M('Hai già tanti soldi con te.¶Non posso dartene altri.'),                                                     # 26
    M('PRELEVA'),                                                                                                  # 27
    M('DEPOSITA'),                                                                                                 # 28
    M('CAMBIA'),                                                                                                   # 29
    M('ESCI'),                                                                                                     # 30
    M('In TV danno un talk show sul precariato.¶Tre ospiti, zero soluzioni.¶Meglio uscire.',
      twin='In TV parlano ancora delle dimissioni del Presidente.¶Nessuno ha capito niente, tutti hanno un’opinione.'),   # 31
    M('Arancini al ragù, specialità di mamma.¶A Catania sono maschili, che si sappia.'),                           # 32
    M('Un lavello lucidissimo.¶Mamma lo pulisce quando è nervosa. Quindi sempre.',
      twin='Un lavello lucidissimo.¶Dalle tue dimissioni, mamma lo pulisce due volte al giorno.'),                 # 33
    M('Dentro il frigo: acqua, limonata e un biglietto.¶“Mangia, che sei magro.”'),                                # 34
    M('Il Puparu stira una camicia con cura chirurgica.¶Non dice una parola: è un mimo, del resto.',
      twin='Il Puparu stira una camicia in silenzio.¶Ha smesso di guardare il telegiornale.'),                     # 35
    M('Il Leccu si è sdraiato sul divano come un nobile in pensione.¶Ti lancia uno sguardo di sufficienza.',
      twin='Il Leccu dorme sul divano.¶Dalle tue dimissioni occupa il tuo posto.'),                                # 36
]

BANCHI = {
    'MAP_CT_MISTERBIANCO_CUBBAR': dict(banco='msg_0603_T25SP0101', num=603, gemello='msg_0870', num_gem=870, messaggi=CUBBAR),
    'MAP_CT_CATANIA_CASA_PROTAGONISTA_2F': dict(banco='msg_0546_T20R0202', num=546, gemello='msg_0851', num_gem=851, messaggi=CAMERA),
    'MAP_CT_CATANIA_CASA_PROTAGONISTA_1F': dict(banco='msg_0545_T20R0201', num=545, gemello='msg_0850', num_gem=850, messaggi=CASA),
}
