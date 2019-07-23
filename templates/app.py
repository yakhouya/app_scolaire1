#Importation
from flask import Flask, render_template, url_for, request, flash,redirect
import psycopg2 as psy

#Création de l'application avec la variable app
app = Flask (__name__)
app.secret_key = "message"

def connectionDB():
    try:
        #connection a la base de donnee
        connection=psy.connect(host= "localhost",
                                database="",
                                user="postgres",
                                password="",
                                port ="5432"
                            )
        return connection
    except (Exception) as error:
        print(" Probléme de connection au serveur ",error)
con=connectionDB()
curseur=con.cursor()
#@app.route permet de préciser à quelle adresse ce qui suit va s’appliquer
@app.route('/')
def accueil():
    return render_template('pages/accueil.html')


@app.route('/formulaire', methods=['GET', 'POST'])
def formulaire():
    curseur.execute("SELECT id_promo, nom_promo FROM promotion")
    apprenant = curseur.fetchall()
    if request.method == "POST":
        flash('Insertion réussit')
        details = request.form
        nom_app = details['nom_ap']
        prenom_app = details['prenom_ap']
        email_app = details['email']
        age_app = details['age']
        matricule = details['matricule']
        sexe = details['sexe']
        idpromo = int(details['promo'])
        requete_ajouter_ap="INSERT INTO apprenant(nom_ap,prenom_ap,email,age,matricule,sexe, id_promo) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        curseur.execute(requete_ajouter_ap,(nom_app, prenom_app, email_app, age_app, matricule, sexe ,idpromo))
        con.commit()
    return render_template('pages/formulaire.html',ap = apprenant)

#Insérer nouveau référent
@app.route('/nouveau_ref', methods=['GET', 'POST'])
def nouveau_ref():
    if request.method == "POST":
        flash('Insertion réussit')
        details = request.form
        nom_ref = details['nom']
        requete_ajouter_ref="INSERT INTO referentiel(nom_ref) VALUES (%s)"
        curseur.execute(requete_ajouter_ref,(nom_ref,))
        con.commit()
    return render_template('pages/nouveau_ref.html')
#Insérer nouveau promo
@app.route('/nouveau_promo', methods=['GET', 'POST'])
def nouveau_promo():
    #Selection des promos
    curseur.execute("SELECT id_ref, nom_ref FROM referentiel")
    promos = curseur.fetchall()
    if request.method == "POST":
        flash('Insertion réussit')
        details = request.form
        nom_promo = details['nom']
        datedebut = details['debut']
        datefin = details['fin']
        idref = int(details['referent'])
        requete_ajouter_promo="INSERT INTO promotion(nom_promo,date_deb,date_fin, id_ref) VALUES (%s,%s,%s,%s)"
        curseur.execute(requete_ajouter_promo,(nom_promo, datedebut, datefin,idref))
        con.commit()
    return render_template('pages/nouveau_promo.html',p = promos)

"""@app.route('/modifierref', methods=['GET', 'POST'])
def modifierref():
    if request.method == "POST":
        details = request.form
        nom_promo = details['nom_promo']
        date_deb = details['date_deb']
        date_fin = details['date_fin']
        requete_ajout_promo="INSERT INTO promotion(nom_promop,date_deb,date_fin) VALUES ( %s,%s, %s)"
        curseur.execute(requete_ajout_promo,(nom_promo,date_deb,date_fin))
        con.commit()
        curseur.close()
    return render_template('modifierref')

"""

#.route('/'):demande de la page d'accueil
#Permet d'ajouter des méta-données:information supplémentaire pour configurer la fonction


@app.route('/nav')
def nav():
    return render_template('partials/_nav.html')

@app.route('/modification', methods=['GET', 'POST'])
def modification():
    curseur.execute("select apprenant.id_ap, apprenant.nom_ap, apprenant.prenom_ap, apprenant.email, apprenant.age, apprenant.matricule, apprenant.sexe,promotion.nom_promo from apprenant, promotion where apprenant.id_promo = promotion.id_promo")
    lister = curseur.fetchall()
    
    curseur.execute("SELECT id_promo ,nom_promo FROM promotion")
    lister1 = curseur.fetchall()
    
    if request.method == "POST":
        flash('Modification réussit')
        details = request.form
        id_ap = details['id_ap']
        nom_app = details['nom_ap']
        prenom_app = details['prenom_ap']
        email_app = details['email']
        age_app = details['age']
        matricule = details['matricule']
        sexe = details['sexe']
        id_promo = int(details['promo'])
        curseur.execute("""
               UPDATE apprenant
               SET nom_ap=%s, prenom_ap=%s, email=%s, age=%s, matricule=%s, sexe=%s, id_promo=%s
               WHERE id_ap=%s
            """, (nom_app, prenom_app, email_app, age_app, matricule, sexe, id_promo,id_ap))
        con.commit()
        curseur.execute("select apprenant.id_ap, apprenant.nom_ap, apprenant.prenom_ap, apprenant.email, apprenant.age, apprenant.matricule, apprenant.sexe,promotion.nom_promo from apprenant, promotion where apprenant.id_promo = promotion.id_promo")
        lister2 = curseur.fetchall()
        return render_template('pages/modifier.html', l=lister2, l1=lister1)
    return render_template('pages/modifier.html', l=lister, l1=lister1)#fonction qui permet de retourner un template

@app.route('/annulation', methods = ['GET','POST'])
def annulation():
    curseur.execute("SELECT * FROM apprenant")
    lister = curseur.fetchall()
    return render_template('pages/annuler.html', l=lister)
 
@app.route('/suspendre', methods = ['GET', 'POST'])
def suspendre():
    curseur.execute("SELECT * FROM apprenant")
    lister = curseur.fetchall()
    return render_template('pages/suspendre.html', l=lister)

@app.route('/modifier_ref', methods=['GET','POST'])
def modifier_ref():
    curseur.execute("SELECT * FROM referentiel")
    lister = curseur.fetchall()
    if request.method == "POST":
        flash('Modification réussit')
        details = request.form
        id_ref = details['id_ref']
        nom_ref = details['nom']
        curseur.execute("""
               UPDATE referentiel
               SET nom_ref=%s
               WHERE id_ref=%s
            """, (nom_ref,id_ref))
        con.commit()
        curseur.execute("SELECT * FROM referentiel")
        lister1 = curseur.fetchall()
        return render_template('pages/modifier_ref.html', l=lister1)
    return render_template('pages/modifier_ref.html', l=lister)

@app.route('/modifier_promo', methods=['GET','POST'])
def modifier_promo():
    curseur.execute("SELECT * FROM promotion")
    lister = curseur.fetchall()
    return render_template('pages/modifier_promo.html', l=lister)

@app.route('/lister_promo', methods=['GET', 'POST'])
def lister_promo():
    curseur.execute("SELECT * FROM promotion")
    lister = curseur.fetchall()
    return render_template('pages/lister.html', l=lister)

#Gérer les erreurs avec 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

#Exécution de l'application avec run()
if (__name__) == '__main__':
    app.run(debug=True, port=3000)   #acivation du serveur directement pas besoin de redémarrer l'app
