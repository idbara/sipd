from flask import Flask, render_template, flash, redirect, url_for, send_from_directory, session, request
app = Flask(__name__, static_url_path='')
from app import app
from datetime import datetime

import pymysql
import os
import config
db = config.get_connection()
cur = db.cursor()


@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        return dashboard()
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return dashboard()
    if request.method == 'POST':
        username  = request.form['username']
        password  = request.form['password']
        cur.execute("SELECT * FROM users WHERE user_nm='"+username+"' AND user_pwd='"+username+"' ")

        if cur.rowcount == 1:
            user = cur.fetchone()
            session['username'] = user[1]
            session['nama_lengkap'] = user[3]
            session['prev'] = user[4]
            session['telpon'] = user[5]
            session['email'] = user[6]
            session['idskpd'] = user[7]
            waktunya=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cur.execute("UPDATE users SET user_lastlog=NULL WHERE user_nm='"+username+"' ")
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('index'))

    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('prev', None)
    session.pop('telpon', None)
    session.pop('email', None)
    session.pop('idskpd', None)
    return redirect(url_for('dashboard'))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        if session['prev'] == 'admin':
            cur.execute("SELECT * FROM users")
            jmluser = cur.rowcount
            return render_template('dashboard.html', title='Dashboard', jmluser=jmluser)
        else:
            return render_template('dashboard-op.html', title='Dashboard')

    else:
        return redirect(url_for('index'))

#users
@app.route('/users')
def users():
    if 'username' in session:

        if session['prev'] == 'admin':
            cur.execute("SELECT * FROM `users` INNER JOIN unors on users.unor_id = unors.id")
            data = cur.fetchall()

            return render_template('users/users.html', title='Pengguna', data=data)
            pass
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/usersTambah')
def usersTambah():
    if 'username' in session:

        if session['prev'] == 'admin':
            cur.execute("SELECT * FROM `unors`")
            skpd = cur.fetchall()

            return render_template('users/userstambah.html', title='Tambah Pengguna', optionskpd=skpd)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/usersInsert', methods=['GET', 'POST'])
def usersInsert():
    if 'username' in session:

        if session['prev'] == 'admin':
            nama = request.form['nama']
            username = request.form['username']
            password = request.form['password']
            skpd = request.form['skpd']
            telfon = request.form['telfon']
            email = request.form['email']
            prev = request.form['prev']
            cur.execute("INSERT INTO `users` (`id`, `user_nm`, `user_pwd`, `user_namalengkap`, `user_prev`, `user_hp`, `user_mail`, `unor_id`, `user_lastlog`, `user_public_ip`) VALUES (NULL,  '"+username+"', '"+password+"', '"+nama+"', '"+prev+"', '"+telfon+"', '"+email+"', '"+skpd+"', NULL, '"+request.remote_addr+"')")
            
            return redirect(url_for('users'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/usersupdate', methods=['GET'])
def usersupdate():
    if 'username' in session:

        if session['prev'] == 'admin':
            id = request.args.get('id')
            cur.execute("SELECT * FROM `users` WHERE `id` = '"+id+"'")
            data = cur.fetchone()

            cur.execute("SELECT * FROM `unors`")
            skpd = cur.fetchall()

            return render_template('users/usersupdate.html', title='Update Pengguna', data=data, optionskpd=skpd)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/usersEdit', methods=['GET', 'POST'])
def usersEdit():
    if 'username' in session:

        if session['prev'] == 'admin':
            idedit = request.args.get('id')
            nama = request.form['nama']
            username = request.form['username']
            password = request.form['password']
            skpd = request.form['skpd']
            telfon = request.form['telfon']
            email = request.form['email']
            prev = request.form['prev']
            cur.execute("UPDATE `users` SET user_nm='"+username+"', `user_pwd` = '"+password+"', `user_namalengkap` = '"+nama+"',user_prev='"+prev+"', user_hp='"+telfon+"',user_mail='"+email+"', unor_id='"+skpd+"'  WHERE `id` = '"+idedit+"'")
            
            return redirect(url_for('users'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/usersDel', methods=['GET', 'POST'])
def usersDel():
    if 'username' in session:

        if session['prev'] == 'admin':
            iddel = request.args.get('id')
            cur.execute("DELETE FROM `users` WHERE `users`.`id` = '"+iddel+"'")
            

            return redirect(url_for('users'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#skpd
@app.route('/skpd')
def skpd():
    if 'username' in session:

        if session['prev'] == 'admin':
            cur.execute("SELECT * FROM `unors`")
            data = cur.fetchall()

            return render_template('skpd/skpd.html', title='SKPD', data=data)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/skpdTambah')
def skpdTambah():
    if 'username' in session:

        if session['prev'] == 'admin':
            cur.execute("SELECT * FROM `unors`")
            skpd = cur.fetchall()

            return render_template('skpd/skpdtambah.html', title='Tambah Pengguna', optionskpd=skpd)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/skpdInsert', methods=['GET', 'POST'])
def skpdInsert():
    if 'username' in session:

        if session['prev'] == 'admin':
            nama = request.form['nama']
            singkat = request.form['singkat']
            cur.execute("INSERT INTO `unors` (`id`, unor_skt, unor_nama) VALUES (NULL,  '"+singkat+"', '"+nama+"')")
            
            return redirect(url_for('skpd'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/skpdEdit', methods=['GET'])
def skpdupdate():
    if 'username' in session:

        if session['prev'] == 'admin':
            id = request.args.get('id')
            cur.execute("SELECT * FROM `unors` WHERE `id` = '"+id+"'")
            data = cur.fetchone()

            return render_template('skpd/skpdupdate.html', title='Update SKPD', data=data)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/skpdUpdate', methods=['GET', 'POST'])
def skpdEdit():
    if 'username' in session:

        if session['prev'] == 'admin':
            idedit = request.args.get('id')
            nama = request.form['nama']
            singkat = request.form['singkat']
            cur.execute("UPDATE `unors` SET unor_skt='"+singkat+"', `unor_nama` = '"+nama+"' WHERE `id` = '"+idedit+"'")
            
            return redirect(url_for('skpd'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/skpdDel', methods=['GET', 'POST'])
def skpdDel():
    if 'username' in session:

        if session['prev'] == 'admin':
            iddel = request.args.get('id')
            cur.execute("DELETE FROM `unors` WHERE `unors`.`id` = '"+iddel+"'")
            

            return redirect(url_for('skpd'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

#input data
@app.route('/inputdatawajib')
def inputdatawajib():
    if 'username' in session:

        if session['prev'] == 'admin':
            cur.execute("SELECT * FROM `unors`")
            data = cur.fetchall()

            return render_template('inputdata/inputdata.html', title='SKPD', data=data)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/inputdata/<idkelompok>', methods=['GET', 'POST'])
def inputdata(idkelompok):
    if 'username' in session:
        idurusan = request.args.get('urusan')
        idheader = request.args.get('header')
        idvariabel = request.args.get('variabel')
        idelement = request.args.get('element')
        idsubelement = request.args.get('subelement')
        idsubsubelement = request.args.get('subsubelement')
        idsubsubsubelement = request.args.get('subsubsubelement')
        tahun = request.args.get('tahun')
        if session['prev'] == 'admin':
            cur.execute("SELECT * FROM `kelompoks` WHERE `id` = '"+idkelompok+"'")
            kelompok = cur.fetchone()[1]
            cur.execute("SELECT * FROM `urusan` WHERE `kelompok` = '"+idkelompok+"'")
            urusan = cur.fetchall()
            cur.execute("SELECT * FROM `header` WHERE `urusan` = '"+str(idurusan)+"'")
            header = cur.fetchall()
            cur.execute("SELECT * FROM `header` WHERE `idheader` = '"+str(idheader)+"'")
            headerselect = cur.fetchone()

            cur.execute("SELECT * FROM `variabel` WHERE `header` = '"+str(idheader)+"'")
            variabel = cur.fetchall()
            cur.execute("SELECT * FROM `variabel` WHERE `idvariabel` = '"+str(idvariabel)+"'")
            variabelselect = cur.fetchone()

            #cur.execute("SELECT * FROM `element` WHERE `variabel` = '"+str(idvariabel)+"'")
            cur.execute("SELECT * FROM `element` JOIN transaksis on transaksis.element = element.idelement JOIN unors on transaksis.data_skpd = unors.id WHERE element.variabel = '"+str(idvariabel)+"'")
            element = cur.fetchall()
            cur.execute("SELECT * FROM `element` WHERE `idelement` = '"+str(idelement)+"'")
            elementselect = cur.fetchone()

            cur.execute("SELECT * FROM `subelement` WHERE `element` = '"+str(idelement)+"'")
            subelement = cur.fetchall()
            cur.execute("SELECT * FROM `subelement` WHERE `idsubelement` = '"+str(idsubelement)+"'")
            subelementselect = cur.fetchone()

            cur.execute("SELECT * FROM `subsubelement` WHERE `subelement` = '"+str(idsubelement)+"'")
            subsubelement = cur.fetchall()
            cur.execute("SELECT * FROM `subsubelement` WHERE `idsubsubelement` = '"+str(idsubsubelement)+"'")
            subsubelementselect = cur.fetchone()

            cur.execute("SELECT * FROM `subsubsubelement` WHERE `subsubelement` = '"+str(idsubsubelement)+"'")
            subsubsubelement = cur.fetchall()
            cur.execute("SELECT * FROM `subsubsubelement` WHERE `idsubsubsubelement` = '"+str(idsubsubsubelement)+"'")
            subsubsubelementselect = cur.fetchone()
            return render_template('inputdata/inputdata.html', title='Input '+str(kelompok), headerselect=headerselect, variabelselect=variabelselect, elementselect=elementselect,subelementselect=subelementselect, subsubelementselect=subsubelementselect,subsubsubelementselect=subsubsubelementselect,idkelompok=idkelompok, pilihurusan=urusan, pilihheader=header, idurusan=str(idurusan),idheader=str(idheader),idvariabel=str(idvariabel),idelement=str(idelement),idsubelement=str(idsubelement),idsubsubelement=str(idsubsubelement),idsubsubsubelement=str(idsubsubsubelement), tahun=tahun, kelompok=str(kelompok), variabel=variabel, element=element, subelement=subelement, subsubelement=subsubelement,subsubsubelement=subsubsubelement)
        else:
            idskpd = session['idskpd']
            cur.execute("SELECT * FROM `kelompoks` WHERE `id` = '"+idkelompok+"'")
            kelompok = cur.fetchone()[1]
            cur.execute("SELECT * FROM `urusan` WHERE `kelompok` = '"+idkelompok+"'")
            urusan = cur.fetchall()
            cur.execute("SELECT * FROM `header` WHERE `urusan` = '"+str(idurusan)+"'")
            header = cur.fetchall()
            cur.execute("SELECT * FROM `header` WHERE `idheader` = '"+str(idheader)+"'")
            headerselect = cur.fetchone()

            cur.execute("SELECT * FROM `variabel` WHERE `header` = '"+str(idheader)+"'")
            variabel = cur.fetchall()
            cur.execute("SELECT * FROM `variabel` WHERE `idvariabel` = '"+str(idvariabel)+"'")
            variabelselect = cur.fetchone()

            #cur.execute("SELECT * FROM `element` WHERE `variabel` = '"+str(idvariabel)+"'")
            cur.execute("SELECT * FROM `element` JOIN transaksis on transaksis.element = element.idelement JOIN unors on transaksis.data_skpd = unors.id WHERE element.variabel = '"+str(idvariabel)+"' AND transaksis.data_skpd ='"+str(idskpd)+"'")
            element = cur.fetchall()
            cur.execute("SELECT * FROM `element` WHERE `idelement` = '"+str(idelement)+"'")
            elementselect = cur.fetchone()

            cur.execute("SELECT * FROM `subelement` WHERE `element` = '"+str(idelement)+"'")
            subelement = cur.fetchall()
            cur.execute("SELECT * FROM `subelement` WHERE `idsubelement` = '"+str(idsubelement)+"'")
            subelementselect = cur.fetchone()

            cur.execute("SELECT * FROM `subsubelement` WHERE `subelement` = '"+str(idsubelement)+"'")
            subsubelement = cur.fetchall()
            cur.execute("SELECT * FROM `subsubelement` WHERE `idsubsubelement` = '"+str(idsubsubelement)+"'")
            subsubelementselect = cur.fetchone()

            cur.execute("SELECT * FROM `subsubsubelement` WHERE `subsubelement` = '"+str(idsubsubelement)+"'")
            subsubsubelement = cur.fetchall()
            cur.execute("SELECT * FROM `subsubsubelement` WHERE `idsubsubsubelement` = '"+str(idsubsubsubelement)+"'")
            subsubsubelementselect = cur.fetchone()
            return render_template('inputdata/inputdata.html', title='Input '+str(kelompok),idskpd=str(idskpd), headerselect=headerselect, variabelselect=variabelselect, elementselect=elementselect,subelementselect=subelementselect, subsubelementselect=subsubelementselect,subsubsubelementselect=subsubsubelementselect,idkelompok=idkelompok, pilihurusan=urusan, pilihheader=header, idurusan=str(idurusan),idheader=str(idheader),idvariabel=str(idvariabel),idelement=str(idelement),idsubelement=str(idsubelement),idsubsubelement=str(idsubsubelement),idsubsubsubelement=str(idsubsubsubelement), tahun=tahun, kelompok=str(kelompok), variabel=variabel, element=element, subelement=subelement, subsubelement=subsubelement,subsubsubelement=subsubsubelement)
    else:
        return redirect(url_for('index'))

@app.route('/inputdataEdit/<idkelompok>', methods=['GET', 'POST'])
def inputdataEdit(idkelompok):
    if 'username' in session:
        idtransaksi = request.args.get('transaksi')
        idurusan = request.args.get('urusan')
        idheader = request.args.get('header')
        idvariabel = request.args.get('variabel')
        idelement = request.args.get('element')
        idsubelement = request.args.get('subelement')
        idsubsubelement = request.args.get('subsubelement')
        idsubsubsubelement = request.args.get('subsubsubelement')
        tahun = request.args.get('tahun')
        if session['prev'] == 'admin':
            cur.execute("SELECT * FROM `kelompoks` WHERE `id` = '"+idkelompok+"'")
            kelompok = cur.fetchone()[1]
            cur.execute("SELECT * FROM `urusan` WHERE `kelompok` = '"+idkelompok+"'")
            urusan = cur.fetchall()
            cur.execute("SELECT * FROM `header` WHERE `urusan` = '"+str(idurusan)+"'")
            header = cur.fetchall()
            cur.execute("SELECT * FROM `header` WHERE `idheader` = '"+str(idheader)+"'")
            headerselect = cur.fetchone()

            cur.execute("SELECT * FROM `variabel` WHERE `header` = '"+str(idheader)+"'")
            variabel = cur.fetchall()
            cur.execute("SELECT * FROM `variabel` WHERE `idvariabel` = '"+str(idvariabel)+"'")
            variabelselect = cur.fetchone()

            #cur.execute("SELECT * FROM `element` WHERE `variabel` = '"+str(idvariabel)+"'")
            cur.execute("SELECT * FROM `element` JOIN transaksis on transaksis.element = element.idelement JOIN unors on transaksis.data_skpd = unors.id WHERE element.variabel = '"+str(idvariabel)+"'")
            element = cur.fetchall()
            cur.execute("SELECT * FROM `element` WHERE `idelement` = '"+str(idelement)+"'")
            elementselect = cur.fetchone()

            cur.execute("SELECT * FROM `subelement` WHERE `element` = '"+str(idelement)+"'")
            subelement = cur.fetchall()
            cur.execute("SELECT * FROM `subelement` WHERE `idsubelement` = '"+str(idsubelement)+"'")
            subelementselect = cur.fetchone()

            cur.execute("SELECT * FROM `subsubelement` WHERE `subelement` = '"+str(idsubelement)+"'")
            subsubelement = cur.fetchall()
            cur.execute("SELECT * FROM `subsubelement` WHERE `idsubsubelement` = '"+str(idsubsubelement)+"'")
            subsubelementselect = cur.fetchone()

            cur.execute("SELECT * FROM `subsubsubelement` WHERE `subsubelement` = '"+str(idsubsubelement)+"'")
            subsubsubelement = cur.fetchall()
            cur.execute("SELECT * FROM `subsubsubelement` WHERE `idsubsubsubelement` = '"+str(idsubsubsubelement)+"'")
            subsubsubelementselect = cur.fetchone()

            cur.execute("SELECT * FROM `transaksis` WHERE `id` = '"+str(idtransaksi)+"'")
            transaksi = cur.fetchone()

            cur.execute("SELECT * FROM `unors`")
            skpd = cur.fetchall()

            return render_template('inputdata/inputdataEdit.html', title='Edit',skpd=skpd,idtransaksi=idtransaksi, transaksi=transaksi, headerselect=headerselect, variabelselect=variabelselect, elementselect=elementselect,subelementselect=subelementselect, subsubelementselect=subsubelementselect,subsubsubelementselect=subsubsubelementselect,idkelompok=idkelompok, pilihurusan=urusan, pilihheader=header, idurusan=str(idurusan),idheader=str(idheader),idvariabel=str(idvariabel),idelement=str(idelement),idsubelement=str(idsubelement),idsubsubelement=str(idsubsubelement),idsubsubsubelement=str(idsubsubsubelement), tahun=tahun, kelompok=str(kelompok), variabel=variabel, element=element, subelement=subelement, subsubelement=subsubelement,subsubsubelement=subsubsubelement)
        else :
            cur.execute("SELECT * FROM `kelompoks` WHERE `id` = '"+idkelompok+"'")
            kelompok = cur.fetchone()[1]
            cur.execute("SELECT * FROM `urusan` WHERE `kelompok` = '"+idkelompok+"'")
            urusan = cur.fetchall()
            cur.execute("SELECT * FROM `header` WHERE `urusan` = '"+str(idurusan)+"'")
            header = cur.fetchall()
            cur.execute("SELECT * FROM `header` WHERE `idheader` = '"+str(idheader)+"'")
            headerselect = cur.fetchone()

            cur.execute("SELECT * FROM `variabel` WHERE `header` = '"+str(idheader)+"'")
            variabel = cur.fetchall()
            cur.execute("SELECT * FROM `variabel` WHERE `idvariabel` = '"+str(idvariabel)+"'")
            variabelselect = cur.fetchone()

            #cur.execute("SELECT * FROM `element` WHERE `variabel` = '"+str(idvariabel)+"'")
            cur.execute("SELECT * FROM `element` JOIN transaksis on transaksis.element = element.idelement JOIN unors on transaksis.data_skpd = unors.id WHERE element.variabel = '"+str(idvariabel)+"'")
            element = cur.fetchall()
            cur.execute("SELECT * FROM `element` WHERE `idelement` = '"+str(idelement)+"'")
            elementselect = cur.fetchone()

            cur.execute("SELECT * FROM `subelement` WHERE `element` = '"+str(idelement)+"'")
            subelement = cur.fetchall()
            cur.execute("SELECT * FROM `subelement` WHERE `idsubelement` = '"+str(idsubelement)+"'")
            subelementselect = cur.fetchone()

            cur.execute("SELECT * FROM `subsubelement` WHERE `subelement` = '"+str(idsubelement)+"'")
            subsubelement = cur.fetchall()
            cur.execute("SELECT * FROM `subsubelement` WHERE `idsubsubelement` = '"+str(idsubsubelement)+"'")
            subsubelementselect = cur.fetchone()

            cur.execute("SELECT * FROM `subsubsubelement` WHERE `subsubelement` = '"+str(idsubsubelement)+"'")
            subsubsubelement = cur.fetchall()
            cur.execute("SELECT * FROM `subsubsubelement` WHERE `idsubsubsubelement` = '"+str(idsubsubsubelement)+"'")
            subsubsubelementselect = cur.fetchone()

            cur.execute("SELECT * FROM `transaksis` WHERE `id` = '"+str(idtransaksi)+"'")
            transaksi = cur.fetchone()
            
            cur.execute("SELECT * FROM `unors`")
            skpd = cur.fetchall()

            return render_template('inputdata-op/inputdataEdit.html', title='Edit',skpd=skpd,idtransaksi=idtransaksi, transaksi=transaksi, headerselect=headerselect, variabelselect=variabelselect, elementselect=elementselect,subelementselect=subelementselect, subsubelementselect=subsubelementselect,subsubsubelementselect=subsubsubelementselect,idkelompok=idkelompok, pilihurusan=urusan, pilihheader=header, idurusan=str(idurusan),idheader=str(idheader),idvariabel=str(idvariabel),idelement=str(idelement),idsubelement=str(idsubelement),idsubsubelement=str(idsubsubelement),idsubsubsubelement=str(idsubsubsubelement), tahun=tahun, kelompok=str(kelompok), variabel=variabel, element=element, subelement=subelement, subsubelement=subsubelement,subsubsubelement=subsubsubelement)


        
        pass
    else:
        return redirect(url_for('index'))

@app.route('/inputdataUpdate/<idkelompok>', methods=['GET', 'POST'])
def inputdataUpdate(idkelompok):
    if 'username' in session:
        if request.method == 'POST':
            idtransaksi = request.form['idtransaksi']
            urusan = request.form['urusan']
            header = request.form['header']
            variabel = request.form['variabel']
            tahun = request.form['tahun']
            status = request.form['status']
            nilai = request.form['nilai']
            satuan = request.form['satuan']
            sumberdata = request.form['sumberdata']
            cur.execute("UPDATE `transaksis` SET `nilai` = '"+nilai+"', `data_skpd` = '"+sumberdata+"' WHERE `transaksis`.`id` = '"+idtransaksi+"';")
            if status == "subsubsubelement":
                cur.execute("UPDATE `subsubsubelement` SET `satuan` = '"+satuan+"' WHERE idsubsubsubelement = '"+request.form['idsubsubsubelement']+"';")
                db.commit()
            elif status == "subsubelement":
                cur.execute("UPDATE `subsubelement` SET `satuan` = '"+satuan+"' WHERE idsubsubelement = '"+request.form['idsubsubelement']+"';")
                db.commit()
            elif status == "subelement":
                cur.execute("UPDATE `subelement` SET `satuan` = '"+satuan+"' WHERE idsubelement = '"+request.form['idsubelement']+"';")
                db.commit()
            elif status == "element":
                idelement = request.form['idelement']
                cur.execute("UPDATE `element` SET `satuan` = '"+satuan+"' WHERE idelement = '"+idelement+"'")
                db.commit()
                #?urusan=1&tahun=2018&header=102&variabel=513
            return redirect('/inputdata/'+idkelompok+'?urusan='+urusan+'&tahun='+tahun+'&header='+header+'&variabel='+variabel)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
        