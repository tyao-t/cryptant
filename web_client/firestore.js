const {Firestore} = require('@google-cloud/firestore');
//require('dotenv').config();
//const CREDENTIALS = JSON.parse(process.env.GOOGLE_CREDENTIALS);
const firestore = new Firestore({
});

async function deleteCollection(db, collectionPath, batchSize) {
  const collectionRef = db.collection(collectionPath);
  const query = collectionRef.orderBy('__name__').limit(batchSize);

  return new Promise((resolve, reject) => {
    deleteQueryBatch(db, query, resolve).catch(reject);
  });
}

async function deleteQueryBatch(db, query, resolve) {
  const snapshot = await query.get();

  const batchSize = snapshot.size;
  if (batchSize === 0) {
    // When there are no documents left, we are done
    resolve();
    return;
  }

  // Delete documents in a batch
  const batch = db.batch();
  snapshot.docs.forEach((doc) => {
    batch.delete(doc.ref);
  });
  await batch.commit();

  // Recurse on the next process tick, to avoid
  // exploding the stack.
  process.nextTick(() => {
    deleteQueryBatch(db, query, resolve);
  });
}

/*
async function vioa(name) {
    const document = firestore.doc(`violation/${name}`);
    const doc = await document.get();
    if (doc._fieldsProto) {
        console.log(doc._fieldsProto)

        let cur_cnt = parseInt(doc._fieldsProto.count.integerValue);
        await document.update({
            count: cur_cnt + 1
        });
        return cur_cnt + 1;
    } else {
        await document.set({
          count: 1
        });
        return 1;
    }
    await document.set({
      word: ["abc", "def", "ckg"]
    });
    console.log('Entered new data into the document');

    /*await document.update({
      body: 'My first Firestore app',
    });
    console.log('Updated an existing document');
    //console.log(doc);
    /*let col = await firestore.listCollections()
    console.log(col.length)
    let res = await deleteCollection(firestore, "test", 5); 
    //console.log("here")
    //await document.delete();
    //console.log('Deleted the document');
} */

async function get_user(phone_num) {
    const document = firestore.doc(`users/${phone_num}`);
    const doc = await document.get();
    console.log(doc)
    return doc;
    /*if (!doc._fieldsProto) {
        return [];
    } else {
        //console.log(doc._fieldsProto.words.arrayValue.values)
        let retVal = []
        for (let i=0;i<doc._fieldsProto.words.arrayValue.values.length;++i) {
            retVal.push(doc._fieldsProto.words.arrayValue.values[i].stringValue)
        }
        //console.log(retVal)
        return retVal
    }*/
}

async function add_user(phone_num, f, l, code) {
  const document = firestore.doc(`users/${phone_num}`);
  const doc = await document.get();
  if (!doc._fieldsProto) {
      await document.set({
          bfname: f,
          blname: l,
          fname: "",
          lname: "",
          activated: "n",
          code: code
      });
  } else {
      await document.update({
          bfname: f,
          blname: l,  
          code: code
      });
  }
}

async function activate_user(phone_num, code) {
  const document = firestore.doc(`users/${phone_num}`);
  const doc = await document.get();
  if (!doc._fieldsProto) {
      await document.set({
          bfname: "",
          blname: "",
          fname: "",
          lname: "",
          activated: "y",
          code: code
      });
      return "true";
  } else {
      if (code !== doc._fieldsProto.code.stringValue) return "false";
      await document.update({
          fname: doc._fieldsProto.bfname.stringValue,
          lname: doc._fieldsProto.blname.stringValue,  
          activated: "y",
      });
      return "true";
  }
}

//add_proh("text_proh", "bitch")

//retrieve_proh("text_proh");

async function clear_all() {
    let col = await firestore.listCollections()
    console.log(col)
    for (let i=0;i<col.length;++i) {
        //console.log(col[i]._queryOptions.collectionId)
        if (col[i]._queryOptions.collectionId === "prohibition") continue;
        deleteCollection(firestore, col[i]._queryOptions.collectionId, 5)
    }
}

exports.clear_all = clear_all;
exports.activate_user = activate_user
exports.get_user = get_user
exports.add_user = add_user